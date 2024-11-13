from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.utils.html import format_html

from django.contrib import admin

from .models import Organisation, Dataset, Resource

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ["id","name", "display_name", "description"]
    search_fields = ["name", "display_name", "title", "description"]

admin.site.register(Organisation, OrganisationAdmin)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ["id","name", "title","organisation","metadata_modified", "tag_list", "resource_downloads"]
    search_fields = ["name", "title", "tags__name"]
    list_filter = (
        ("tags__name", DropdownFilter),
        ("organisation", RelatedDropdownFilter),
        ("license_title", DropdownFilter)
    )
    list_select_related = ["organisation"]
    date_hierarchy = "metadata_modified"
    ordering = ("-metadata_modified",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'resource_set')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def resource_downloads(self, obj):
        return format_html(" | ".join("<a href='%s' target='_blank'>%s</a>" % (r.download_link, r.format) for r in obj.resource_set.all()))

admin.site.register(Dataset, DatasetAdmin)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "dataset", "name", "format", "date_created"]
    search_fields = ["name"]
    list_filter = (
        ("dataset__organisation", RelatedDropdownFilter),
        ("format", DropdownFilter),
    )
    list_select_related = ["dataset", "dataset__organisation"]

    date_hierarchy = "date_created"
    ordering = ("-date_created",)

admin.site.register(Resource, ResourceAdmin)