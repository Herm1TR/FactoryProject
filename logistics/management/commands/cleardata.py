from django.core.management.base import BaseCommand
from logistics.models import LogisticsData, Dock

class Command(BaseCommand):
    help = 'Clear all LogisticsData and/or Dock data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--logisticsdata',
            action='store_true',
            help='Clear all LogisticsData records'
        )
        parser.add_argument(
            '--dock',
            action='store_true',
            help='Clear all Dock records'
        )

    def handle(self, *args, **options):
        if options['logisticsdata']:
            count, _ = LogisticsData.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully cleared {count} LogisticsData records"))
        if options['dock']:
            count, _ = Dock.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully cleared {count} Dock records"))
        if not options['logisticsdata'] and not options['dock']:
            self.stdout.write(self.style.WARNING("Please specify at least one option: --logisticsdata or --dock"))
