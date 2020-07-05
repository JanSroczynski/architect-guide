from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import ArchitectureProject, Architect, Photo


class RegisterUserForm(ModelForm):
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Repeat password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 're_password')
        labels = {
            'password': 'Password',
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'email',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None

    def clean_re_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['re_password']:
            raise ValidationError('Passwords must match')
        return self.cleaned_data['re_password']


class AddProjectForm(ModelForm):
    architect_name = forms.CharField(max_length=128, required=False)
    architect_description = forms.CharField(widget=forms.Textarea(), required=False)
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['architect'].required = False

    class Meta:
        model = ArchitectureProject
        fields = (
            'photo', 'name', 'description', 'adress', 'city', 'country', 'project_category', 'architect', 'latitude',
            'longitude')
        widgets = {'latitude': forms.HiddenInput, 'longitude': forms.HiddenInput}

    def clean_architect(self):
        if self.cleaned_data['architect']:
            return self.cleaned_data['architect']
        if not self.data['architect_name'] or not self.data['architect_descripton']:
            raise ValidationError('These fields must not be empty')
        return self.cleaned_data['architect']

    def save(self, commit=True):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        adress = self.cleaned_data['adress']
        country = self.cleaned_data['country']
        project_category = self.cleaned_data['project_category']
        architect = self.cleaned_data['architect']
        architect_name = self.cleaned_data['architect_name']
        architect_description = self.cleaned_data['architect_description']
        photo = self.cleaned_data['photo']
        latitude = self.cleaned_data['latitude']
        longitude = self.cleaned_data['longitude']
        created_by = self.user
        if architect == '':
            architect = Architect.objects.create(name=architect_name, description=architect_description)
        new_project = ArchitectureProject.objects.create(name=name, description=description, latitude=latitude,
                                                         longitude=longitude, country=country,
                                                         adress=adress, architect=architect, added_by=created_by)
        for category in project_category:
            new_project.project_category.add(category)
        Photo.objects.create(category=1, architecture_project=new_project, created_by=created_by,
                             path=self.cleaned_data["photo"], title=True)
        return new_project
