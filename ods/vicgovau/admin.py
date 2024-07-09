from django.contrib import admin

from .models import Organisation, Dataset

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ["id","name", "display_name", "description"]
    search_fields = ["name", "display_name", "title", "description"]

admin.site.register(Organisation, OrganisationAdmin)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ["id","name", "title","organisation","metadata_modified"]
    search_fields = ["name", "title"]
    list_filter = ["organisation", "license_title"]
    select_related=["organisation"]

admin.site.register(Dataset, DatasetAdmin)
