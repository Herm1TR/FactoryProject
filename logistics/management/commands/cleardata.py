from django.core.management.base import BaseCommand
from logistics.models import LogisticsData, Dock

class Command(BaseCommand):
    help = '清除所有 LogisticsData 與 / 或 Dock 的資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--logisticsdata',
            action='store_true',
            help='清除所有 LogisticsData 資料'
        )
        parser.add_argument(
            '--dock',
            action='store_true',
            help='清除所有 Dock 資料'
        )

    def handle(self, *args, **options):
        if options['logisticsdata']:
            count, _ = LogisticsData.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"已清除 {count} 筆 LogisticsData 資料"))
        if options['dock']:
            count, _ = Dock.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"已清除 {count} 筆 Dock 資料"))
        if not options['logisticsdata'] and not options['dock']:
            self.stdout.write(self.style.WARNING("請至少指定一個選項：--logisticsdata 或 --dock"))
