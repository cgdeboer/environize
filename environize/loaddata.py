import os
import json
from django.conf import settings
from django.core.management.color import no_style
from django.db import connections, models

RELATIONALS = [models.ForeignKey, models.OneToOneField]


def _scrub_fields(data, Model):
    fields = {}
    m2m_fields = {}
    for name, value in data.items():
        model_attribute = getattr(Model, name)
        model_field = getattr(model_attribute, 'field', None)
        if model_field and any([isinstance(model_field, x)
                                for x in RELATIONALS]):
            fields['{}_id'.format(name)] = value
        elif model_field and isinstance(model_field, models.ManyToManyField):
            m2m_fields[name] = value
        else:
            fields[name] = value
    return fields, m2m_fields


def _get_model(apps, model_str):
    app, model = model_str.split('.')
    return apps.get_model(app, model)


def _create_instance(data, apps):
    pk = data.pop('pk', None)
    Model = _get_model(apps, data.pop('model'))
    fields, m2m_fields = _scrub_fields(data['fields'], Model)
    if pk:
        instance, _ = Model.objects.get_or_create(pk=pk, defaults=fields)
    else:
        instance = Model.objects.create(**fields)
    for field, values in m2m_fields.items():
        getattr(instance, field).add(*values)
    return instance, Model


def _reset_sequence(Model):
    connection = connections['default']
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Model])
    if sequence_sql:
        with connection.cursor() as cursor:
            for line in sequence_sql:
                cursor.execute(line)


def loaddata(apps, rel_fixture_path):
    with open(os.path.join(settings.BASE_DIR, rel_fixture_path)) as fixture:
        data = json.load(fixture)
        results = [_create_instance(x, apps) for x in data]
    for model in set([x[1] for x in results]):
        _reset_sequence(model)
    return [x[0] for x in results]
