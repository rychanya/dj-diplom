import json

from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {}
        with open(settings.DUMP_FILE, encoding="utf-8", mode="w") as file:
            for name in settings.DUMP_MODELS_NAMES:
                qs = getattr(models, name).objects.all()
                data[name] = serializers.serialize("json", qs)
            json.dump(data, file)
