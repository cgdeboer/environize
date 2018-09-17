from django.db import models


class Foo(models.Model):
    name = models.CharField(max_length=128)


class Baz(models.Model):
    foo = models.ForeignKey("app.Foo", on_delete=models.CASCADE)
    bars = models.ManyToManyField("app.Bar")


class Bar(models.Model):
    name = models.CharField(max_length=128)
    ham = models.OneToOneField("app.Ham", on_delete=models.CASCADE)


class Ham(models.Model):
    name = models.CharField(max_length=128)
