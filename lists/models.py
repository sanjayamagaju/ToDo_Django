from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import date


class TodoList(models.Model):
    title = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, null=True, related_name="todolists", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.format_date_with_ordinal(date.today())
        super().save(*args, **kwargs)

    def format_date_with_ordinal(self, dt):
        day = dt.day
        suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        day_str = str(day).lstrip("0")
        return f'{day_str}{suffix} {dt.strftime("%B %Y")}'

    def count(self):
        return self.todos.count()

    def count_finished(self):
        return self.todos.filter(is_finished=True).count()

    def count_open(self):
        return self.todos.filter(is_finished=False).count()


class Todo(models.Model):
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, null=True, related_name="todos", on_delete=models.CASCADE
    )
    todolist = models.ForeignKey(
        TodoList, related_name="todos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.description

    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()

    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()
