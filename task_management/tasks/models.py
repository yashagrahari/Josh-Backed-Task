from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator, 
    MaxLengthValidator, 
)

from django.core.exceptions import ValidationError
from .validators import (
    validate_task_name, 
    validate_description_length, 
)


class Task(models.Model):
    """
    Enhanced Task model with comprehensive validation
    """
    TASK_TYPES = [
        ('development', 'Development'),
        ('design', 'Design'),
        ('research', 'Research'),
        ('other', 'Other')
    ]

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold')
    ]

    name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(3, "Task name must be at least 3 characters long."),
            MaxLengthValidator(200, "Task name cannot exceed 200 characters."),
            validate_task_name
        ]
    )
    description = models.TextField(
        blank=True, 
        null=True,
        validators=[validate_description_length]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    task_type = models.CharField(
        max_length=20, 
        choices=TASK_TYPES, 
        default='other',
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='not_started',
    )
    
    # Many-to-Many relationship with User
    assigned_users = models.ManyToManyField(User, related_name='users_tasks')

    def clean(self):
        """
        Additional model-level validation
        """
        super().clean()
        
        # Validate completed_at
        if self.completed_at and self.completed_at < self.created_at:
            raise ValidationError({
                'completed_at': "Completion date cannot be before creation date."
            })
        
        # Ensure status and completed_at are consistent
        if self.status == 'completed' and not self.completed_at:
            raise ValidationError({
                'completed_at': "Completed tasks must have a completion date."
            })

    def save(self, *args, **kwargs):
        """
        Perform full validation before saving
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name