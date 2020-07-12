from django.db import models


class Specialization(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)


class Stat(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)


class SpecializationStat(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING)
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)
    value = models.IntegerField()


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, default=True)
    telegram_id = models.IntegerField()
    language_code = models.CharField(max_length=10, null=True)
    is_bot = models.BooleanField()

    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING, null=True)


class UserStat(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)
