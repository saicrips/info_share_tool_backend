from django.db import models

from . import User


class Team(models.Model):
    name = models.CharField(verbose_name="name", max_length=64)
    description = models.CharField(verbose_name="description", max_length=200)
    administrators = models.ManyToManyField(
        User, through="TeamAdministrator", related_name="administrators"
    )
    members = models.ManyToManyField(User, through="TeamMember", related_name="members")
    created_at = models.TimeField(
        verbose_name="created_at", auto_now_add=True, editable=False
    )
    changed_at = models.TimeField(
        verbose_name="changed_at", auto_now=True, editable=False
    )

    def __str__(self):
        return self.name


class TeamAdministrator(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
