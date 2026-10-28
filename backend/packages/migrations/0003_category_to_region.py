from django.db import migrations


def move_old_categories(apps, schema_editor):
    """Old versions stored 'india'/'international' in category. Move them to region."""
    Package = apps.get_model("packages", "Package")
    for old in ("india", "international"):
        Package.objects.filter(category=old).update(region=old, category="holiday")


class Migration(migrations.Migration):
    dependencies = [("packages", "0002_package_region_package_suits_halal_and_more")]
    operations = [migrations.RunPython(move_old_categories, migrations.RunPython.noop)]
