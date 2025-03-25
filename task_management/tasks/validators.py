from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_task_name(value):
    """
    Comprehensive task name validation
    """
    # Prevent empty or overly generic task names
    forbidden_names = [
        'task', 'todo', 'untitled', 'new task', 
        'placeholder', '', 'test', 'draft'
    ]
    
    if value.lower().strip() in forbidden_names:
        raise ValidationError(
            _('Please provide a more descriptive task name.'),
            code='invalid_task_name'
        )

def validate_description_length(value):
    """
    Ensure description is not too short or too long
    """
    word_count = len(value.split())
    if word_count < 3:
        raise ValidationError(
            _('Description must be at least 3 words long.'),
            code='description_too_short'
        )
    if word_count > 200:
        raise ValidationError(
            _('Description cannot exceed 200 words.'),
            code='description_too_long'
        )
