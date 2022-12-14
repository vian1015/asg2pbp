from django.urls import path
from todolist.views import show_todolist
from todolist.views import register
from todolist.views import login_user
from todolist.views import logout_user
from todolist.views import add_task
from todolist.views import delete_task
from todolist.views import inverse_checkbox
from todolist.views import show_json

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add/', add_task, name='add_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('inverse_checkbox/<int:task_id>/', inverse_checkbox, name='inverse_checkbox'),
    path('json/', show_json, name='show_json')
]