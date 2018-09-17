import six
from django.test import TestCase, modify_settings
from django.core.management import call_command
from tests.project.app.models import Ham


class TestEnvFilterMethods(TestCase):

    def setUp(self):
        out = six.StringIO()
        call_command("migrate", "app", "zero", stdout=out)

    def checkobject(self, env):
        hams = Ham.objects.all()
        return hams.count() == 1 and hams.filter(name=env).exists()

    @modify_settings(ALLOWED_HOSTS={'remove': 'testserver'})
    def test_only_in(self):
        out = six.StringIO()
        call_command("migrate", "app", "0001", stdout=out)
        for env in ["production", "dev", "qa"]:
            with self.settings(ENVIRONMENT=env):
                call_command("migrate", "app", "0002", stdout=out)
                self.assertTrue(self.checkobject(env))
                call_command("migrate", "app", "0001", stdout=out)

    def test_only_test(self):
        out = six.StringIO()
        call_command("migrate", "app", "0001", stdout=out)
        with self.settings(ENVIRONMENT="test"):
            call_command("migrate", "app", "0002", stdout=out)
            self.assertTrue(self.checkobject("test"))
            call_command("migrate", "app", "0001", stdout=out)

    @modify_settings(ALLOWED_HOSTS={'remove': 'testserver'})
    def test_except_in(self):
        out = six.StringIO()
        call_command("migrate", "app", "0002", stdout=out)
        Ham.objects.all().delete()
        for env in ["production", "dev", "qa"]:
            with self.settings(ENVIRONMENT=env):
                call_command("migrate", "app", "0003", stdout=out)
                self.assertTrue(self.checkobject("not-test"))
                call_command("migrate", "app", "0002", stdout=out)

    def test_except_test(self):
        out = six.StringIO()
        call_command("migrate", "app", "0002", stdout=out)
        Ham.objects.all().delete()
        with self.settings(ENVIRONMENT="test"):
            call_command("migrate", "app", "0003", stdout=out)
            self.assertEqual(Ham.objects.count(), 0)
            call_command("migrate", "app", "0002", stdout=out)

    def tearDown(self):
        out = six.StringIO()
        call_command("migrate", "app", "zero", stdout=out)
