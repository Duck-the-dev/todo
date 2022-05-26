from django.contrib import admin

# Register your models here.
from todo_app.models import ToDoItem, ToDoList, Completed

admin.site.register(ToDoItem)
admin.site.register(ToDoList)
admin.site.register(Completed)
