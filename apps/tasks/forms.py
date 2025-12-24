from django import forms

from apps.tasks.models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""

    class Meta:
        model = Task
        fields = ['name', 'status', 'priority', 'deadline']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter task description',
                    'maxlength': 255,
                }
            ),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        task = super().save(commit=False)
        if self.project:
            task.project = self.project
        if commit:
            task.save()
        return task


class TaskCreateForm(forms.Form):
    """Simplified form for creating new tasks via HTMX."""

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-custom',
                'placeholder': 'Start typing here to create a task...',
                'required': True,
            }
        ),
    )

    priority = forms.ChoiceField(
        choices=Task.Priority.choices,
        initial=Task.Priority.MEDIUM,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-custom',
            }
        ),
    )

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control form-control-custom',
                'type': 'datetime-local',
            }
        ),
    )


class TaskUpdateForm(forms.ModelForm):
    """Form for updating task details."""

    class Meta:
        model = Task
        fields = ['name', 'priority', 'deadline']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'required': True,
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm',
                }
            ),
            'deadline': forms.DateTimeInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'type': 'datetime-local',
                }
            ),
        }
