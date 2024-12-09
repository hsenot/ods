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

class IsDatashareFilter(admin.SimpleListFilter):
    title = 'Datashare?'
    parameter_name = 'is_datashare'

    def lookups(self, request, model_admin):
        return (
            (True, 'Yes'),
            (False, 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.extra(where=["(download_link like \'https://datashare%%\') = %s"], params=[value,])
        return queryset


class DataServerFilter(admin.SimpleListFilter):
    title = 'Data server'
    parameter_name = 'data_server'

    def lookups(self, request, model_admin):
        return ((y,y) for y in sorted(list(set([x.download_link.split("/")[2] for x in Resource.objects.filter(download_link__isnull=False)]))))

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(download_link__contains=value)
        return queryset



class ResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "dataset", "get_organisation", "get_format", "get_datashare", "date_created"]
    search_fields = ["name", "dataset__name", "download_link"]
    list_filter = (
        ("dataset__organisation", RelatedDropdownFilter),
        ("format", DropdownFilter),
        IsDatashareFilter,
        DataServerFilter,
    )
    list_select_related = ["dataset", "dataset__organisation"]

    date_hierarchy = "date_created"
    ordering = ("-date_created",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.extra(select={ 'datashare': "download_link like 'https://datashare%%'" })

    def get_organisation(self, obj):
        return obj.dataset.organisation
    get_organisation.short_description = "Organisation"

    def get_format(self, obj):
        return format_html("<a href='%s' target='_blank'>%s</a>" % (obj.download_link, obj.format))
    get_organisation.short_description = "Format / download"

    def get_datashare(self, obj):
        return obj.datashare
    get_datashare.short_description = "Datashare?"
    get_datashare.boolean = True


admin.site.register(Resource, ResourceAdmin)