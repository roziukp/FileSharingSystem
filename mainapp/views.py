from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.core.mail import send_mail
from django.conf import settings
from . import models
from django.contrib import auth
from django.contrib import messages


class Registration(View):
    template_name = 'mainapp/registration.html'
    form_class = forms.UserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():

            users = models.Profile.objects.all()
            username_list = [i.username for i in users]
            email_list = [i.email for i in users]

            if request.POST.get('username') not in username_list and request.POST.get('email') not in email_list:
                form.save()

                newuser = auth.authenticate(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'], )
                if newuser is not None:
                    auth.login(request, newuser)
                    messages.success(request, 'User has been registered!')
                return redirect('/', {'message': messages})

                # from_email = settings.EMAIL_HOST_USER
                # to_email = profile.email
                # message = 'Welcome, {} thanks for registration!'.format(profile.username)
                # send_mail('', message=message, from_email=from_email, recipient_list=[to_email])

            else:
                error_message = 'User with this username or email is already exists! Try another username'
                return render(request, self.template_name, {'form': form,
                                                            'error_message': error_message
                                                            })


class Login(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user=user)
            messages.success(request, 'User is logged!')
            return redirect('/')
        else:
            self.context['error'] = 'Login error! Try again'
            return render(request, 'index.html', self.context)


def registered_users(request):
    context = dict()
    context['users'] = models.Profile.objects.all()
    return render(request, 'mainapp/chatroom.html', context)


class AddFile(View):
    template_name = 'mainapp/add_file.html'
    form_class = forms.FilesForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            fileform = form.save(commit=False)
            fileform.user = models.Profile.objects.last()
            fileform.save()
            return render(request, self.template_name, {'form': form,
                                                        'success': 'File was succesfuly added!'})

        else:
            error_message = 'Something is wrong with your data!'
            return render(request, self.template_name, {'form': form,
                                                        'eror_message': error_message})
