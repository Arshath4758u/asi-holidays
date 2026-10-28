from django.core.management.base import BaseCommand

from insights.services import build_report, email_report


class Command(BaseCommand):
    help = "Build the weekly insights report (last N full days) and email it to the team."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7)
        parser.add_argument("--no-email", action="store_true")

    def handle(self, *args, **opts):
        report = build_report(opts["days"])
        sent = False if opts["no_email"] else email_report(report)
        self.stdout.write(report.summary)
        self.stdout.write(self.style.SUCCESS(f"Saved report {report.period_start} to {report.period_end}. Emailed: {sent}"))