import uuid

from django.db import models

from .abstract_models import AbstractModel


class Review(AbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='reviews')
