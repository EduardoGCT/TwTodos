from django.views.generic import ListView, CreateView

from .models import Todo

class TodoListView(ListView):
    model = Todo

class TodoCreateView(CreateView):
    model = Todo
    fields = ["title", "deadline"]