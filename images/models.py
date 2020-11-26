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
