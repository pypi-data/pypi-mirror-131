# Generated by Django 3.2 on 2021-04-28 09:03

from django.db import migrations, models
import rescape_region.model_helpers
import rescape_region.models.search_location


class Migration(migrations.Migration):

    dependencies = [
        ('rescape_region', '0025_alter_settings_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('identification', models.JSONField(default=rescape_region.models.search_location.default_search_identification)),
                ('street', models.JSONField(default=rescape_region.models.search_location.default_search_street)),
                ('geojson', models.JSONField(default=rescape_region.model_helpers.feature_collection_default)),
                ('data', models.JSONField(default=rescape_region.model_helpers.region_data_default)),
            ],
        ),
    ]
