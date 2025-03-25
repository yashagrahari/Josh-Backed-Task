from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 
            'name', 
            'description', 
            'created_at', 
            'completed_at', 
            'task_type', 
            'status', 
            'assigned_users',
        ]
        read_only_fields = ['created_at']

    def validate_name(self, value):
        """
        Additional name validation
        """
        # Prevent duplicate task names (case-insensitive)
        existing_tasks = Task.objects.filter(name__iexact=value)
        if existing_tasks.exists():
            raise serializers.ValidationError(
                ("A task with this name already exists.")
            )
        return value

    def validate(self, data):
        """
        Cross-field validation
        """
        # Validate status and completion
        if data.get('status') == 'completed' and not data.get('completed_at'):
            raise serializers.ValidationError({
                'completed_at': ("Completed tasks must have a completion date.")
            })

        return data

class TaskAssignmentSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_user_ids(self, value):
        """
        Validate user IDs
        """
        unique_user_ids = list(set(value))
        
        existing_users = User.objects.filter(id__in=unique_user_ids)
        
        if len(existing_users) != len(unique_user_ids):
            raise serializers.ValidationError(
                _("One or more user IDs are invalid.")
            )
        
        return unique_user_ids
    