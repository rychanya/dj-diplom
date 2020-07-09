import json
import os

from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.User.objects.all().delete()
        models.User.objects.create_superuser("admin", "admin@example.com", "admin")

        if os.path.isfile(settings.DUMP_FILE):
            with open(settings.DUMP_FILE, encoding="utf-8", mode="r") as file:
                json_data = json.load(file)
        else:
            self.stdout.write(f"{settings.DUMP_FILE} not exists")
            exit()

        for name in settings.DUMP_MODELS_NAMES:
            data = serializers.deserialize("json", json_data[name])
            for obj in data:
                obj.save()
