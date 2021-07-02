# Generated by Django 3.2.4 on 2021-07-01 22:11

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('realestate', '0004_offerpage_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='realestate.OfferPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
