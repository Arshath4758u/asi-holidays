from django.db import migrations

PLACEHOLDER = "[POLICY TEXT TO BE SUPPLIED BY ASI HOLIDAYS]"


def seed(apps, schema_editor):
    SiteSettings = apps.get_model("content", "SiteSettings")
    PolicyPage = apps.get_model("content", "PolicyPage")
    SiteSettings.objects.get_or_create(pk=1)
    for slug in ("privacy", "terms", "cancellation"):
        PolicyPage.objects.get_or_create(slug=slug, defaults={"body": PLACEHOLDER})


class Migration(migrations.Migration):
    dependencies = [("content", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
