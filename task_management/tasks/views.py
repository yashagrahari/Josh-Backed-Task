import logging
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer, TaskAssignmentSerializer
from .error_handling import UserNotFoundException

# Configure logger
logger = logging.getLogger(__name__)

class TaskCreateView(APIView):
    def post(self, request):
        """
        Enhanced task creation with detailed logging
        """
        try:
            logger.info(f"Attempting to create task")

            with transaction.atomic():
                serializer = TaskSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            
            logger.info(f"Task created successfully: {serializer.data.get('id')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Task creation failed: {str(e)}", exc_info=True)
            return Response({'error': 'Task creation failed', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskAssignView(APIView):
    def post(self, request, task_id):
        """
        Enhanced task assignment with comprehensive error handling
        """
        try:
            task = Task.objects.get(pk=task_id)
            logger.info(f"Attempting to assign task {task_id}")

            serializer = TaskAssignmentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user_ids = serializer.validated_data['user_ids']
            users = User.objects.filter(id__in=user_ids)

            if users.count() != len(user_ids):
                raise UserNotFoundException(f"Some user IDs are invalid: {user_ids}")
            
            with transaction.atomic():
                task.assigned_users.add(*users)
                task.save()

            logger.info(f"Task {task_id} assigned to {len(users)} users successfully")
            return Response({'message': f'Task assigned to {len(users)} users', 'task': TaskSerializer(task).data}, status=status.HTTP_200_OK)
        
        except UserNotFoundException as unfe:
            logger.warning(str(unfe))
            return Response({'error': 'User Assignment Error', 'detail': str(unfe)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Task assignment failed: {str(e)}", exc_info=True)
            return Response({'error': 'Task Assignment Failed', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserTaskView(APIView):
    def get(self, request, user_id):
        """
        Return tasks for a specific user with error logging
        """
        try:
            logger.info(f"Retrieving tasks for user {user_id}")
            User.objects.get(id=user_id)

            tasks = Task.objects.filter(assigned_users__id=user_id)

            return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            logger.warning(f"Attempted to retrieve tasks for non-existent user {user_id}")
            return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving user tasks: {str(e)}", exc_info=True)
            return Response({'error': 'Error retrieving user tasks', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
