from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Set urls that are older than 30 days to expired"

    def handle_noargs(self, **options):
        from url.models import Url
        from django.utils import timezone
        import datetime
        urls = Url.objects.filter(pub_date__lte=timezone.now() - datetime.timedelta(days=30))
        for url in urls:
            url.delete()