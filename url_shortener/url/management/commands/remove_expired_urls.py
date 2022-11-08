from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Set urls that are older than 30 days to expired"

    def handle(self, *args, **options):
        from url.models import Url
        from django.utils import timezone
        import datetime
        urls = Url.objects.filter(last_access__lte=timezone.now() - datetime.timedelta(days=30))
        deleted_count = 0
        for url in urls:
            url.delete()
            print("Deleted url: " + url.original_url + " last access: " + str(url.last_access) + " with shorten url: " + url.shorten_url + " pub date: " + str(url.pub_date) + " count: " + str(url.count))
            deleted_count += 1
        print("Deleted " + str(deleted_count) + " expired urls")