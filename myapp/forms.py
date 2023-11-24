from django import forms

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Task title", max_length=200)
    description = forms.CharField(widget=forms.Textarea, label="Task description")

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Project title", max_length=200)

