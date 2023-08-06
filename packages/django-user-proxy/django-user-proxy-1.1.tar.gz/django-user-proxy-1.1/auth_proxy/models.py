from django.db import models


class UserProxy(models.Model):
    """
    User proxy model, represents a local instance of
    a user object from another database.
    """
    user_id = models.UUIDField()
