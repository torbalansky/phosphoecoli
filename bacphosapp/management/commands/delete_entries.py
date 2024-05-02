from django.core.management.base import BaseCommand
from bacphosapp.models import PhosphoProtein

class Command(BaseCommand):
    help = 'Delete all entries from the PhosphoProtein model'

    def handle(self, *args, **options):
        PhosphoProtein.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All entries deleted successfully'))
