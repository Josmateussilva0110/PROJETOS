from django.urls import path #type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('new_task/', views.new_task, name='new_task'),
    path('tasks/<task_id>/', views.task, name='task'),
    path('new_notation/<task_id>/', views.new_notation, name='new_notation'),
    path('edit_notation/<notation_id>/', views.edit_notation, name='edit_notation'),
    path('delete_task/<task_id>/', views.delete_task, name='delete_task'),
    path('delete_notation/<notation_id>/', views.delete_notation, name='delete_notation'),
    path('my_day/', views.my_day, name='my_day'),
    path('tasks_important/', views.tasks_important, name='tasks_important'),
    path('mark_important/<task_id>/', views.mark_important, name='mark_important'),
    path('mark_completed/<task_id>/', views.mark_completed, name='mark_completed'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('restore_task/<task_id>/', views.restore_task, name='restore_task'),
    path('remove_important/<task_id>', views.remove_important, name='remove_important'),
]
