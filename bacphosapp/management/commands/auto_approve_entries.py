from django.core.management.base import BaseCommand
from bacphosapp.models import PhosphoProtein

class Command(BaseCommand):
    help = 'Automatically approve all entries in the PhosphoProtein model'

    def handle(self, *args, **options):
        PhosphoProtein.objects.all().update(approved=True)

        self.stdout.write(self.style.SUCCESS('All entries approved successfully'))
