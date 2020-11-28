import logging

from .models import Template, TemplateStore

logger = logging.getLogger(__name__)


def update_url_and_text_in_template(template: dict, url: str, text: str) -> dict:
    """
    Given strings, `url` and `text`, set URL and text in the `template`

    Sample Template:
        {'height': 600,
         'objects': [{'height': 300,
                      'type': 'image',
                      'url': '',
                      'width': 350,
                      'x': 300,
                      'y': 300},
                     {'height': 100,
                      'text': '',
                      'type': 'textbox',
                      'width': 300,
                      'x': 400,
                      'y': 300}],
         'width': 600}

    Returns: Dictionary reflecting updated template
    """
    for item in list(template.values()):
        try:
            for record in item:
                if record.get('type') == 'image':
                    record['url'] = url
                elif record.get('type') == 'textbox':
                    record['text'] = text
        except TypeError:
            pass

    logger.info(
        f'Updated url to {url} and text to {text} in the following template: {template}'
    )
    return template


def generate_data_templates_from_csv_data(csv_file) -> None:
    """
    Given CSV file, iterate over the data and generate final template that can be used as request body for IGS API

    The final template must be stored in `Template` Django model since storing them in memory can cause out of memory
    issues for large data sets.

    Flow:
        - Given the CSV file, iterate over all the rows (except first one, assuming first one is the headers)
        - For each row of data, iterate over all the templates available in the TemplateStore table
        - Substitute the `url` and `text` value from the data in the row in to the Template and store that template
        - Mark that template as `processed=False`. Later when this will be actually processed (i.e. passed through
        IGS API), we will mark it as `processed=True`
    """
    import csv

    with open(csv_file, 'r') as csv_data:
        reader = csv.reader(csv_data)
        next(reader, None)  # skip the headers
        for row in reader:
            price, url = row[1], row[-1]

            # For all templates in TemplateStore
            #
            for template_store_object in TemplateStore.objects.all():
                template_with_substituted_url_and_price = update_url_and_text_in_template(
                    template=template_store_object.template, url=url, text=f'Now at ${price}')

                data_template_obj = Template.objects.create(
                    csv_file_name=csv_file, processed=False, template=template_with_substituted_url_and_price
                )
                logger.info(
                    f'Created data template: {data_template_obj}'
                )

        logger.info(f'Parsed CSV file: {csv_file} and created data template objects')
