from django.db import models

from . import User, Team


class Channel(models.Model):
    class MembersScope(models.IntegerChoices):
        default = 0, "default"
        limited = 1, "limited"

    name = models.CharField(verbose_name="name", max_length=64)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="description", max_length=200)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    members_scope = models.IntegerField(
        choices=MembersScope.choices, default=MembersScope.default
    )
    members = models.ManyToManyField(
        User, through="ChannelMember", related_name="channel_members"
    )
    created_at = models.TimeField(
        verbose_name="created_at", auto_now_add=True, editable=False
    )
    changed_at = models.TimeField(
        verbose_name="changed_at", auto_now=True, editable=False
    )

    def __str__(self):
        return self.name


class ChannelMember(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
