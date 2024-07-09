# Generated by Django 5.0.6 on 2024-07-09 11:41

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('vicgovau', '0004_dataset_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericStringTaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=36, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='dataset',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='vicgovau.GenericStringTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
