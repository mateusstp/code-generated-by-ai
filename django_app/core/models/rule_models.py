from django.db import models
from .base_models import BaseModel

class Rule(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
