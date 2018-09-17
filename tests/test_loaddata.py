import six
import json
import os
from django.test import TestCase
from django.core.management import call_command
from tests.project.app.models import Ham, Bar, Baz, Foo


PATH = 'tests/project/app/fixtures/'


class TestLoaddataMethods(TestCase):

    def setUp(self):
        out = six.StringIO()
        with self.settings(ENVIRONMENT='dev'):
            call_command("migrate", "app", "0003", stdout=out)
            Ham.objects.all().delete()

    def __check_data(self, data, instances):
        assert len(data) == instances.count()
        assert (set([x.pk for x in instances]) ==
                set([x['pk'] for x in data]))

    def test_loaddata(self):
        out = six.StringIO()
        with self.settings(ENVIRONMENT='dev'):
            call_command("migrate", "app", "0004", stdout=out)

        MODEL_FIXTURES = ((Ham, 'ham.json'),
                          (Bar, 'bar.json'),
                          (Foo, 'foo.json'),
                          (Baz, 'baz.json'))

        for Model, fixture in MODEL_FIXTURES:
            instances = Model.objects.all()
            with open(os.path.join(PATH, fixture)) as rawfile:
                data = json.load(rawfile)
                self.__check_data(data, instances)

    def tearDown(self):
        out = six.StringIO()
        call_command("migrate", "app", "zero", stdout=out)
