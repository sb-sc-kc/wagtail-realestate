# Generated by Django 3.2.5 on 2021-07-06 22:04

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('realestate', '0010_auto_20210706_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleofferpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='realestate.SaleOfferPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]