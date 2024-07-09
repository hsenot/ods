from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

from django.db import models
from django.utils.translation import gettext as _

class Organisation(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(null=False)
    display_name = models.CharField(null=False)
    title = models.CharField(null=False)
    description = models.CharField(null=False)

    def __str__(self):
        return self.display_name


class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=36, verbose_name=_('Object id'), db_index=True)


class Dataset(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(null=False)
    title = models.CharField(null=False)
    license_title = models.CharField(null=True)
    metadata_created = models.DateTimeField(null=False)
    metadata_modified = models.DateTimeField(null=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(through=GenericStringTaggedItem)
