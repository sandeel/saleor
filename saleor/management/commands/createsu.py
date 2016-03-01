from django.core.management.base import BaseCommand
from saleor.userprofile.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.getenv('SUPERUSER_NAME')).exists():
            User.objects.create_superuser(os.getenv('SUPERUSER_NAME'), os.getenv('SUPERUSER_EMAIL'), os.getenv('SUPERUSER_PASS'))

