from django.db import migrations
import environize


@environize.only_in(envs=["production"])
def add_data(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.create(name="production")


@environize.only_in(envs=["dev"])
def add_dev_data(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.create(name="dev")


@environize.only_in(envs=["qa"])
def add_qa_data(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.create(name="qa")


@environize.only_in(envs=["qa", "dev", "production"])
def remove_hams(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.all().delete()


@environize.only_in(envs=["test"])
def add_test_data(apps, schema_editor):
    Ham = apps.get_model("app", "Ham")
    Ham.objects.create(name="test")


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_data, lambda x, y: None),
        migrations.RunPython(add_dev_data, lambda x, y: None),
        migrations.RunPython(add_test_data, lambda x, y: None),
        migrations.RunPython(add_qa_data, remove_hams)
    ]
