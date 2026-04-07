from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Todo


def make_todo(**kwargs):
    """Helper: create a Todo with sensible defaults."""
    defaults = {
        "title": "Test Task",
        "priority": Todo.Priority.MEDIUM,
        "deadline": date.today() + timedelta(days=7),
    }
    defaults.update(kwargs)
    return Todo.objects.create(**defaults)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TodoModelTest(TestCase):
    def test_str(self):
        todo = make_todo(title="Minha Tarefa", priority=Todo.Priority.HIGH)
        self.assertIn("Minha Tarefa", str(todo))
        self.assertIn("Alta", str(todo))

    def test_mark_has_complete_sets_today(self):
        todo = make_todo()
        self.assertIsNone(todo.finished_at)
        todo.mark_has_complete()
        self.assertEqual(todo.finished_at, date.today())

    def test_mark_has_complete_is_idempotent(self):
        yesterday = date.today() - timedelta(days=1)
        todo = make_todo(finished_at=yesterday)
        todo.mark_has_complete()
        # Should NOT overwrite the existing date
        todo.refresh_from_db()
        self.assertEqual(todo.finished_at, yesterday)

    def test_default_priority_is_medium(self):
        todo = Todo.objects.create(
            title="Defaults",
            deadline=date.today() + timedelta(days=3),
        )
        self.assertEqual(todo.priority, Todo.Priority.MEDIUM)

    def test_description_optional(self):
        todo = make_todo()
        self.assertIsNone(todo.description)

    def test_ordering_priority_then_deadline(self):
        d1 = date.today() + timedelta(days=5)
        d2 = date.today() + timedelta(days=1)
        t_low = make_todo(title="Low", priority=Todo.Priority.LOW, deadline=d1)
        t_high = make_todo(title="High", priority=Todo.Priority.HIGH, deadline=d2)
        t_med = make_todo(title="Med", priority=Todo.Priority.MEDIUM, deadline=d1)
        ordered = list(Todo.objects.all())
        # "1"=High < "2"=Medium < "3"=Low
        self.assertEqual(ordered[0], t_high)
        self.assertEqual(ordered[1], t_med)
        self.assertEqual(ordered[2], t_low)


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------


class TodoListViewTest(TestCase):
    def test_empty_list(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há tarefas cadastradas")

    def test_list_shows_todos(self):
        make_todo(title="Tarefa Alpha")
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefa Alpha")

    def test_filter_pending(self):
        make_todo(title="Tarefa Aberta")
        make_todo(title="Tarefa Fechada", finished_at=date.today())
        response = self.client.get(reverse("todo_list") + "?status=pending")
        self.assertContains(response, "Tarefa Aberta")
        self.assertNotContains(response, "Tarefa Fechada")

    def test_filter_completed(self):
        make_todo(title="Tarefa Aberta")
        make_todo(title="Tarefa Fechada", finished_at=date.today())
        response = self.client.get(reverse("todo_list") + "?status=completed")
        self.assertContains(response, "Tarefa Fechada")
        self.assertNotContains(response, "Tarefa Aberta")

    def test_search_by_title(self):
        make_todo(title="Comprar leite")
        make_todo(title="Estudar Django")
        response = self.client.get(reverse("todo_list") + "?q=leite")
        self.assertContains(response, "Comprar leite")
        self.assertNotContains(response, "Estudar Django")

    def test_search_by_description(self):
        make_todo(title="Task A", description="detalhe especial")
        make_todo(title="Task B", description="outro")
        response = self.client.get(reverse("todo_list") + "?q=especial")
        self.assertContains(response, "Task A")
        self.assertNotContains(response, "Task B")


class TodoCreateViewTest(TestCase):
    def test_get_create_form(self):
        response = self.client.get(reverse("todo_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nova Tarefa")

    def test_post_creates_todo(self):
        response = self.client.post(
            reverse("todo_create"),
            {
                "title": "Nova Task",
                "priority": "2",
                "deadline": date.today() + timedelta(days=3),
            },
        )
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.first().title, "Nova Task")

    def test_post_invalid_missing_title(self):
        response = self.client.post(
            reverse("todo_create"),
            {"priority": "M", "deadline": date.today()},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), 0)


class TodoUpdateViewTest(TestCase):
    def test_get_update_form(self):
        todo = make_todo()
        response = self.client.get(reverse("todo_update", kwargs={"pk": todo.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar Tarefa")

    def test_post_updates_todo(self):
        todo = make_todo(title="Original")
        response = self.client.post(
            reverse("todo_update", kwargs={"pk": todo.pk}),
            {"title": "Editada", "priority": "1", "deadline": todo.deadline},
        )
        self.assertRedirects(response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Editada")

    def test_cannot_edit_completed_task_get(self):
        todo = make_todo(finished_at=date.today())
        response = self.client.get(reverse("todo_update", kwargs={"pk": todo.pk}))
        self.assertRedirects(response, reverse("todo_list"))

    def test_cannot_edit_completed_task_post(self):
        todo = make_todo(title="Done", finished_at=date.today())
        response = self.client.post(
            reverse("todo_update", kwargs={"pk": todo.pk}),
            {"title": "Hack", "priority": "3", "deadline": todo.deadline},
        )
        self.assertRedirects(response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Done")


class TodoDeleteViewTest(TestCase):
    def test_get_confirm_delete(self):
        todo = make_todo(title="Para Excluir")
        response = self.client.get(reverse("todo_delete", kwargs={"pk": todo.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Para Excluir")

    def test_post_deletes_todo(self):
        todo = make_todo()
        response = self.client.post(reverse("todo_delete", kwargs={"pk": todo.pk}))
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 0)


class TodoCompleteViewTest(TestCase):
    def test_complete_via_post(self):
        todo = make_todo()
        response = self.client.post(reverse("todo_complete", kwargs={"pk": todo.pk}))
        self.assertRedirects(response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertEqual(todo.finished_at, date.today())

    def test_complete_get_not_allowed(self):
        todo = make_todo()
        response = self.client.get(reverse("todo_complete", kwargs={"pk": todo.pk}))
        self.assertEqual(response.status_code, 405)

    def test_complete_nonexistent_returns_404(self):
        response = self.client.post(reverse("todo_complete", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TodoIntegrationTest(TestCase):
    def test_create_complete_delete_flow(self):
        # 1. Create
        self.client.post(
            reverse("todo_create"),
            {
                "title": "Integration Task",
                "priority": "2",
                "deadline": date.today() + timedelta(days=1),
            },
        )
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertIsNone(todo.finished_at)

        # 2. Complete
        self.client.post(reverse("todo_complete", kwargs={"pk": todo.pk}))
        todo.refresh_from_db()
        self.assertEqual(todo.finished_at, date.today())

        # 3. Attempt edit (should be blocked)
        self.client.post(
            reverse("todo_update", kwargs={"pk": todo.pk}),
            {"title": "Blocked", "priority": "L", "deadline": todo.deadline},
        )
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Integration Task")

        # 4. Delete
        self.client.post(reverse("todo_delete", kwargs={"pk": todo.pk}))
        self.assertEqual(Todo.objects.count(), 0)
