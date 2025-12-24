from django import forms

from apps.projects.models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects."""

    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter project name',
                    'maxlength': 255,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        project = super().save(commit=False)
        if self.user:
            project.user = self.user
        if commit:
            project.save()
        return project


class ProjectCreateForm(forms.Form):
    """Simplified form for creating new projects."""

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
                'required': True,
            }
        ),
    )


class ProjectUpdateForm(forms.Form):
    """Form for updating project name."""

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': True,
            }
        ),
    )
