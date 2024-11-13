import requests
import base64
import logging
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from .models import Organisation, Dataset, Resource

logger = logging.getLogger(__name__)

API = {
    'KEY': settings.APIS['vicgovau']['KEY'],
    'BASE': settings.APIS['vicgovau']['BASE'] 
}


def get_organisations(endpoint='/datavic/opendata/v1.1/organisations'):
    url = "%s%s" % (API['BASE'], endpoint)

    # Set the apikey header
    headers = {
        "apikey": API['KEY']
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        r = response.json()
        for o in r['organisations']:
            logger.debug("Processing organisation: %s" % o['display_name'])
            if 'id' in o:
                obj, created = Organisation.objects.update_or_create(
                    id=o['id'],
                    defaults={
                        'name': o['name'],
                        'display_name': o['display_name'],
                        'title': o['title'],
                        'description': o['description'],
                    }
                )

    else:
        response.raise_for_status()


def get_datasets(endpoint='/datavic/opendata/v1.1/datasets'):
    url = "%s%s" % (API['BASE'], endpoint)

    # Set the apikey header
    headers = {
        "apikey": API['KEY']
    }

    # Reload organisations to account for new ones
    get_organisations()

    # Caching organisation map to avoid 1 query per dataset
    orgs = {o.name: o.id for o in Organisation.objects.all()}

    # Pages are 1-indexed
    page = 1
    while 1:
        response = requests.get(url, headers=headers, params={'page': page})
        
        if response.status_code == 200:
            r = response.json()
            if len(r['datasets']):
                for d in r['datasets']:
                    logger.debug("Processing dataset: %s" % d['name'])
                    if 'id' in d:
                        obj, created = Dataset.objects.update_or_create(
                            id=d['id'],
                            defaults={
                                'name': d['name'],
                                'title': d['title'],
                                'license_title': d.get('license_title'),
                                'metadata_created': timezone.make_aware(datetime.fromisoformat(d['metadata_created'])),
                                'metadata_modified': timezone.make_aware(datetime.fromisoformat(d['metadata_modified'])),
                                'organisation_id': orgs[d['organisation']['name']]
                            }
                        )

                        # Upsert associated downloadable resources
                        if "_embedded" in d and 'resources' in d["_embedded"]:
                            # Recreate resources to account for deletions in source system
                            Resource.objects.filter(dataset_id=d['id']).delete()

                            for r in d["_embedded"]["resources"]:
                                obj2, created2 = Resource.objects.update_or_create(
                                    id=r['id'],
                                    defaults={
                                        'dataset_id': d['id'],
                                        'name': r['name'],
                                        'format': r['format'],
                                        'date_created': timezone.make_aware(datetime.fromisoformat(r['date_created'])),
                                        'download_link': next((x['href'] for x in r['_links'] if x['rel'] == 'download'), None) if '_links' in r else None
                                    }
                                )
                        # Add tags using the taggit API
                        obj.tags.set([t.strip().lower() for t in d['tags']], clear=True)
                        obj.save()

                # Next page please
                page += 1
            else:
                print("No more datasets in the page, time to exit")
                break
        else:
            response.raise_for_status()