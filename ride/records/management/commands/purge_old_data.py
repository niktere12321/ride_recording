from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from records.models import Records


class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        Records.objects.filter(end_time__lte=datetime.now()-timedelta(days=5)).delete()
        self.stdout.write('Deleted objects older than 10 days')
