from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView
from .models import *
from .forms import *


class Index(View):

    def get(self, request):
        queryset = ArchitectureProject.objects.all()
        context = {'data_points': queryset}
        return render(request, 'index.html', context=context)


class ProjectDetail(DetailView):
    model = ArchitectureProject

    def get_project_data(self):
        d = {
            'Project name': self.object.name,
            'Adress': self.object.adress,
            'City': self.object.city,
            'Deigner': self.object.architect.name,
            'Year completed': self.object.year,
            'categories': ', '.join([category.name for category in self.object.project_category.all()]),
        }
        d = ProjectDetail.clean_project_data(d)
        return d

    @staticmethod
    def clean_project_data(d):
        return_d = {}
        for key, value in d.items():
            if value != [] and value is not None and value != "":
                return_d[key] = value
        return return_d

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_data'] = self.get_project_data()
        try:
            context['photo'] = self.object.photo_set.get(title=True)
        except Photo.DoesNotExist:
            context['photo'] = None
        context['likes_nr'] = self.object.user_likes.all()
        return context


class RegisterUser(FormView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        data = form.cleaned_data
        data.pop('re_password')
        User.objects.create_user(**data)
        return super().form_valid(form)


class MyLoginView(LoginView):

    def get_redirect_url(self):
        return reverse_lazy('index')


class UserDetail(DetailView):
    model = User
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.architectureproject_set.all()
        print(context['projects'])
        return context


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name')
    template_name = 'update_user.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy("user_detail", args=(self.object.id,))

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj != self.request.user:
            raise PermissionDenied()
        return obj


class AddProject(LoginRequiredMixin, View):
    def get(self, request):
        context = {'form': AddProjectForm(user=request.user, initial={
            'longitude': request.GET.get('lon'),
            'latitude': request.GET.get('lat')
        }
                                          )}
        return render(request, 'add_project.html', context=context)

    def post(self, request):
        request.GET.get('lon'), request.GET.get('lat')
        form = AddProjectForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            new_project = form.save()
            return redirect(reverse_lazy('project_detail', kwargs={'pk': new_project.id}))
        raise Http404


class Like(LoginRequiredMixin, View):

    def get(self, request, project_id):
        user = request.user
        project = ArchitectureProject.objects.get(pk=project_id)
        user_likes = project.user_likes.all()
        if user not in user_likes:
            project.user_likes.add(user)
        return redirect(reverse_lazy('project_detail', kwargs={'pk': project_id}))


class Unlike(LoginRequiredMixin, View):

    def get(self, request, project_id):
        user = request.user
        project = ArchitectureProject.objects.get(pk=project_id)
        user_likes = project.user_likes.all()
        if user in user_likes:
            project.user_likes.remove(user)
        return redirect(reverse_lazy('project_detail', kwargs={'pk': project_id}))
