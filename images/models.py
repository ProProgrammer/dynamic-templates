from django.db import models


class TemplateStore(models.Model):
    """
    Template store to contain template JSON in JSONField
    """

    name = models.CharField(max_length=30, null=False, blank=False)
    template = models.JSONField()

    def __str__(self) -> str:
        """
        String representation of model object
        """
        return str(self.name)


class Template(models.Model):
    """
    Template object to store templates created from templates in `TemplateStore`
    These templates are created as part of helpers.generate_data_templates_from_csv_data
    """

    csv_file_name = models.CharField(max_length=30, null=False, blank=False)
    processed = models.BooleanField(default=False)
    template = models.JSONField()

    def __str__(self):
        """
        Set the template's str representation to: Template with url <url> and text <text>
        """
        url = text = None
        for item in list(self.template.values()):
            try:
                for record in item:
                    if record.get('type') == 'image':
                        url = record['url']
                    elif record.get('type') == 'textbox':
                        text = record['text']
            except TypeError:
                pass

        return f'Template with url {url} and text {text}'
