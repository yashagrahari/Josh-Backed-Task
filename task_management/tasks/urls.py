from django.urls import path
from .views import TaskCreateView, TaskAssignView, UserTaskView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:task_id>/assign/', TaskAssignView.as_view(), name='task-assign'),
    path('users/<int:user_id>/tasks/', UserTaskView.as_view(), name='user-tasks'),
]
