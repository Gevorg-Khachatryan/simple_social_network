from django.shortcuts import render, redirect
from ssn_main.forms import *
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from ssn_main.models import CustomUser, Post
from django.contrib.auth.views import FormView as ContribFormView
from django.contrib.auth import login

#
# class LoginFormView(FormView):
#     template_name = 'templates/login.html'
#     form_class = UserForm
#     success_url = 'accounts/profile/'
#
#     def form_valid(self, form):
#         form.send_email()
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         print(request,'////')
#         return super().post(self)


class RegistrationView(ContribFormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/accounts/login/")
        form = RegistrationForm()
        return render(request=request, template_name="registration/registration.html", context={"form": form})


class ProfileView(TemplateView):

    template_name = 'profile.html'

    def get(self,request):
        print(request.user)
        return render(request,self.template_name, {'user': request.user})


class PostView(ListView):

    template_name = 'post.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.objects.all()

    # def get(self,request):
    #     print(request.user)
    #     return render(request,self.template_name, {'posts': Post.objects})