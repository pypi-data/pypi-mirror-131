# Generated by Django 3.0.8 on 2020-07-31 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescape_region', '0018_auto_20200619_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='key',
            field=models.CharField(max_length=50),
        ),
        migrations.AddConstraint(
            model_name='project',
            constraint=models.UniqueConstraint(fields=('user', 'deleted', 'key'), name='unique_project_with_deleted'),
        ),
        migrations.AddConstraint(
            model_name='project',
            constraint=models.UniqueConstraint(condition=models.Q(deleted=None), fields=('user', 'key'), name='unique_project_without_deleted'),
        ),
    ]
