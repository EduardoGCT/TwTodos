from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

from .models import Todo


class TodoListView(ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status", "")
        search = self.request.GET.get("q", "").strip()
        if status == "pending":
            qs = qs.filter(finished_at__isnull=True)
        elif status == "completed":
            qs = qs.filter(finished_at__isnull=False)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_filter"] = self.request.GET.get("status", "")
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class TodoCreateView(CreateView):
    model = Todo
    fields = ["title", "description", "priority", "deadline"]
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        messages.success(self.request, "Tarefa criada com sucesso!")
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["title", "description", "priority", "deadline"]
    success_url = reverse_lazy("todo_list")

    def get(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.finished_at:
            messages.warning(request, "Não é possível editar uma tarefa já concluída.")
            return redirect("todo_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.finished_at:
            messages.warning(request, "Não é possível editar uma tarefa já concluída.")
            return redirect("todo_list")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Tarefa atualizada com sucesso!")
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        messages.success(self.request, "Tarefa excluída com sucesso!")
        return super().form_valid(form)


class TodoCompleteView(View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.mark_has_complete()
        messages.success(request, f'Tarefa "{todo.title}" marcada como concluída!')
        return redirect("todo_list")
