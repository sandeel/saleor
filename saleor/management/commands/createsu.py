from django.core.management.base import BaseCommand
from saleor.userprofile.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email=os.getenv('SUPERUSER_EMAIL')).exists():
            User.objects.create_superuser(email=os.getenv('SUPERUSER_EMAIL'), password=os.getenv('SUPERUSER_PASS'))

