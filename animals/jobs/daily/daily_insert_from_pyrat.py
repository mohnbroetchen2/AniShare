from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "Django Daily Cleanup Job"

    def execute(self):
        from django.core import management
management.call_command("clearsessions")