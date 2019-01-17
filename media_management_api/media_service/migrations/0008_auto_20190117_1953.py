# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-17 19:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_service', '0007_auto_20180518_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAdmins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'course_admin',
                'verbose_name_plural': 'course_admins',
            },
        ),
        migrations.CreateModel(
            name='CourseCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[(b'initiated', b'Initiated'), (b'completed', b'Completed'), (b'error', b'Error')], default=b'initiated', max_length=100)),
                ('error', models.TextField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=b'{}')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'course copy',
                'verbose_name_plural': 'course copy',
            },
        ),
        migrations.AlterModelOptions(
            name='mediastore',
            options={'verbose_name': 'media_store', 'verbose_name_plural': 'media_store'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='lti_custom_canvas_api_domain',
        ),
        migrations.AddField(
            model_name='course',
            name='canvas_course_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='sis_course_id',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='iiif_source',
            field=models.CharField(choices=[(b'images', b'Collection Images'), (b'custom', b'IIIF Manifest')], default=b'images', max_length=100),
        ),
        migrations.AddField(
            model_name='coursecopy',
            name='dest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest_copies', to='media_service.Course'),
        ),
        migrations.AddField(
            model_name='coursecopy',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_copies', to='media_service.Course'),
        ),
        migrations.AddField(
            model_name='courseadmins',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_service.Course'),
        ),
        migrations.AddField(
            model_name='courseadmins',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_service.UserProfile'),
        ),
    ]