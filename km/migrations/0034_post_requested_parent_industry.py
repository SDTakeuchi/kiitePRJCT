# Generated by Django 3.1.4 on 2021-10-09 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0033_post_requested_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='requested_parent_industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='km.alumnijobparentcategory'),
        ),
    ]