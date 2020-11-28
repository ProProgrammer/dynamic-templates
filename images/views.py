import json
import logging
import time

import requests
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from images.models import TemplateStore, Template
from images.serializers import TemplateStoreSerializer

logger = logging.getLogger(__name__)


class TemplateStoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing templates
    """

    queryset = TemplateStore.objects.all()
    serializer_class = TemplateStoreSerializer
    pagination_class = None


class ImageGenerationView(APIView):
    """
    POST <image-service-url>,
    Request Body: {"json": <json>}

    Return: to return textual content with values generated from the passed JSON, sample response:
        Mime type image/png
        600px by 600px in dimensions
        Contains a scaled down image of a duck, positioned at (300, 300)
        Contains a text element, ‘Now at $50’, positioned at (400, 300)
    """

    def post(self, request: Request):
        """
        POST <image-service-url>,
        Request Body: {"json": <json>}

        Args:
            request:  request object

        Returns:
            textual content with values generated from the passed JSON
            In reality this would return the actual image along with below characteristics
            Sample Response:
                Mime type image/png
                600px by 600px in dimensions
                Contains a scaled down image of a duck, positioned at (300, 300)
                Contains a text element, ‘Now at $50’, positioned at (400, 300)
        """

        parsed_json = json.loads(request.data.get('json'))
        width = parsed_json.get('width')
        height = parsed_json.get('height')
        mime_type = 'image/png'

        image_x_position = image_y_position = image_text = text_x_position = text_y_position = None

        for item in parsed_json.get('objects'):
            if 'image' in item.values():
                image_x_position = item.get('x')
                image_y_position = item.get('y')
            elif 'textbox' in item.values():
                image_text = item.get('text'),
                text_x_position = item.get('x')
                text_y_position = item.get('y')

        output = list()

        output.append(f'Mime type {mime_type}')
        output.append(f'{height}px by {width}px in dimensions')
        output.append(f'Contains a scaled down image of a duck, positioned at ({image_x_position}, {image_y_position})')
        output.append(f"Contains a text element, '{image_text}' positioned at ({text_x_position}, {text_y_position})")

        # Imitate ~200 second response time by setting a manual 150 millisecond sleep
        time.sleep(0.150)

        return Response(
            ' '.join(output), status=HTTP_200_OK
        )


class DataFeedGenerationView(APIView):
    """
    Generate data feed by triggering images.helpers.process_data_templates
    """

    def get(self, request):
        """
        GET request that triggers `images.helpers.process_data_templates`
        Args:
            request:

        Returns: Response object
        """

        unprocessed_data_templates = Template.objects.filter(processed=False)

        output = []

        if unprocessed_data_templates.exists():

            igs_api_url = request.build_absolute_uri(
                location=reverse('images:image_generation_service')
            )
            headers = {
                'content-type': 'application/json',
            }

            for data_template in unprocessed_data_templates:

                post_request_data = {
                    'json': json.dumps(data_template.template)
                }
                response = requests.post(url=igs_api_url, data=json.dumps(post_request_data), headers=headers)

                if response.status_code == HTTP_200_OK:
                    logger.info(
                        f'Processed data template {data_template} and marked it as processed'
                    )
                    data_template.processed = True
                    data_template.save()

                    # Add IGS API response output to output list and send that list as response to Data Feed
                    # Generation request
                    output.append(response.text)

        if output:
            return Response(output, status=HTTP_200_OK)

        return Response('No data to process. All data templates already processed', status=HTTP_200_OK)
