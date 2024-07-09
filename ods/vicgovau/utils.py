import requests
import base64
import logging
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from .models import Organisation, Dataset

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

    page = 0
    while 1:
        page += 1
        response = requests.get(url, headers=headers, params={'page': page})
        
        if response.status_code == 200:
            r = response.json()
            if len(r['datasets']):
                for d in r['datasets']:
                    logger.debug("Processing dataset: %s" % d['name'])
                    if 'id' in d:
                        try:
                            obj, created = Dataset.objects.update_or_create(
                                id=d['id'],
                                defaults={
                                    'name': d['name'],
                                    'title': d['title'],
                                    'license_title': d.get('license_title'),
                                    'metadata_created': timezone.make_aware(datetime.fromisoformat(d['metadata_created'])),
                                    'metadata_modified': timezone.make_aware(datetime.fromisoformat(d['metadata_modified'])),
                                    'organisation': Organisation.objects.get(name=d['organisation']['name'])
                                }
                            )
                        except KeyError as e:
                            print(d)
                            raise
            else:
                print("No more datasets in the page, time to exit")
                break
        else:
            response.raise_for_status()