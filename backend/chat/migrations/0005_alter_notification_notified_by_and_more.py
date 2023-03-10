# Generated by Django 4.1.2 on 2022-12-12 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_notification_thread_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifiedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notified_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifieduser', to=settings.AUTH_USER_MODEL),
        ),
    ]
