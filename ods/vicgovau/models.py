from django.db import models

class Organisation(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(null=False)
    display_name = models.CharField(null=False)
    title = models.CharField(null=False)
    description = models.CharField(null=False)

    def __str__(self):
        return self.display_name

class Dataset(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(null=False)
    title = models.CharField(null=False)
    license_title = models.CharField(null=True)
    metadata_created = models.DateTimeField(null=False)
    metadata_modified = models.DateTimeField(null=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)
