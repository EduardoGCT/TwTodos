from django.db import models
from datetime import date


class Todo(models.Model):
    class Priority(models.TextChoices):
        HIGH = "1", "Alta"
        MEDIUM = "2", "Média"
        LOW = "3", "Baixa"

    title = models.CharField(
        verbose_name="Título", max_length=100, null=False, blank=False
    )
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    priority = models.CharField(
        verbose_name="Prioridade",
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    deadline = models.DateField(verbose_name="Data de entrega", null=False, blank=False)
    finished_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["priority", "deadline"]

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"

    def mark_has_complete(self):
        if not self.finished_at:
            self.finished_at = date.today()
            self.save()
