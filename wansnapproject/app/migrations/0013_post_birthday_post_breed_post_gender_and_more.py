# Generated by Django 5.1.7 on 2025-06-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_post_dog'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='breed',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
