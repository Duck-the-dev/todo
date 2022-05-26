from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from todo_app.models import ToDoList, ToDoItem, Completed


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context


class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
        'completed_item',
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = ToDoList

    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context


class ItemComplete(UpdateView):
    model = Completed

    def get_success_url(self):
        return reverse("item-complete", args=[self.kwargs["list_id"], self.object.todo_list_id])

    def get_context_data(self, **kwargs):
        context = super(ItemComplete).get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list

        return context


class CompletedView(ListView):
    model = Completed
    template_name = "todo_app/completed.html"

    def apply(self):
        if self.method == "POST":
            if self.POST.get('complete'):
                Completed.objects.create(
                    todo_list=self.POST.get('todo_list'),
                    todo_item=self.POST.get('todo_item'), )

        return render(self, 'todo_app/completed.html')

    def get_success_url(self):
        return reverse_lazy("completed-list", args=[self.kwargs["list_id"]])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

    def get_queryset(self):
        return Completed.objects.filter(todo_list_id=self.kwargs["list_id"])
