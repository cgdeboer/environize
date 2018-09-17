from django.db import migrations
import environize


@environize.except_in(envs=["test"])
def except_test_data(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.create(name="not-test")


def remove_hams(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180916_1122'),
    ]

    operations = [
        migrations.RunPython(except_test_data, remove_hams)
    ]
