# Generated by Django 4.2.4 on 2023-08-20 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_resume_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='pdf',
        ),
    ]
