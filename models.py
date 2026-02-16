from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    """Extended user model for TaskShuffler"""
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    is_registered = models.BooleanField(default=False)
    registered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Admin(models.Model):
    """Admin model - max 5 admins allowed"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.user.user.username}"

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class Task(models.Model):
    """Task model - can be predefined or admin-created"""
    TASK_TYPE_CHOICES = [
        ('predefined', 'Predefined'),
        ('custom', 'Custom'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='predefined')
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class TaskAssignment(models.Model):
    """Task assignment model - tracks who is assigned what task and when"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    week_starting = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.task.title} (Week of {self.week_starting.date()})"

    class Meta:
        verbose_name = "Task Assignment"
        verbose_name_plural = "Task Assignments"
        unique_together = ('task', 'user', 'week_starting')


class TaskHistory(models.Model):
    """Track task assignment history for rotation purposes"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_week = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.user.user.username}"

    class Meta:
        verbose_name = "Task History"
        verbose_name_plural = "Task Histories"
        ordering = ['-assigned_week']


class ShuffleLog(models.Model):
    """Log all shuffle operations for audit purposes"""
    shuffled_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    shuffled_at = models.DateTimeField(auto_now_add=True)
    total_assignments = models.IntegerField()
    week_starting = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Shuffle on {self.shuffled_at.date()} by {self.shuffled_by}"

    class Meta:
        verbose_name = "Shuffle Log"
        verbose_name_plural = "Shuffle Logs"
        ordering = ['-shuffled_at']