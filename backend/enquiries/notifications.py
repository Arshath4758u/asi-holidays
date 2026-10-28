import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_team(enquiry):
    """Email the team about a new enquiry. Never raises: a mail failure must not lose the lead."""
    recipients = settings.ENQUIRY_NOTIFY_EMAILS
    if not recipients:
        return
    when = enquiry.departure_date or enquiry.travel_month or "not given"
    body = (
        f"New enquiry on asiholidays.in\n\n"
        f"Name: {enquiry.name}\n"
        f"WhatsApp: {enquiry.whatsapp_number}\n"
        f"Email: {enquiry.email or '-'}\n"
        f"Destination: {enquiry.destination or '-'}\n"
        f"Package: {enquiry.package or '-'}\n"
        f"Travel: {when}\n"
        f"Travellers: {enquiry.travellers}\n"
        f"Budget: {enquiry.budget or '-'}\n"
        f"Message: {enquiry.message or '-'}\n"
    )
    try:
        send_mail(f"New enquiry: {enquiry.name} - {enquiry.destination or 'general'}", body, settings.DEFAULT_FROM_EMAIL, recipients)
    except Exception:
        logger.exception("Could not send enquiry notification for enquiry %s", enquiry.pk)
