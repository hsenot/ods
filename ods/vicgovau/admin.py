from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

from django.contrib import admin

from .models import Organisation, Dataset

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ["id","name", "display_name", "description"]
    search_fields = ["name", "display_name", "title", "description"]

admin.site.register(Organisation, OrganisationAdmin)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ["id","name", "title","organisation","metadata_modified", "tag_list"]
    search_fields = ["name", "title", "tags__name"]
    list_filter = (
        ("tags__name", DropdownFilter),
        ("organisation", RelatedDropdownFilter),
        ("license_title", DropdownFilter)
    )
    list_select_related=["organisation"]
    date_hierarchy = "metadata_modified"
    ordering = ("-metadata_modified",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Dataset, DatasetAdmin)
