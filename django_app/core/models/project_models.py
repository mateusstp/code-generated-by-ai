from django.db import models
from .base_models import BaseModel

class ProjectGCP(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    # Add additional fields as needed

class ComponentGCP(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    # Add additional fields as needed

class BusinessUnit(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    # Add additional fields as needed
