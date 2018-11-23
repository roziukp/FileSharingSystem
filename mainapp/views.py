from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.core.mail import send_mail
from django.conf import settings
from . import models
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404


# simple registration to default user model
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

            if request.POST.get('username') not in username_list:     # check if user is unique
                profile = form.save()

                newuser = auth.authenticate(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'], )
                if newuser is not None:
                    auth.login(request, newuser)
                    messages.success(request, 'User has been registered!')

                    from_email = settings.EMAIL_HOST_USER
                    to_email = profile.email
                    message = 'Welcome, {} thanks for registration!'.format(profile.username)
                    send_mail('', message=message, from_email=from_email, recipient_list=[to_email])
                    return redirect('/', {'message': messages})

            else:
                error_message = 'User with this username is already exists! Try another username'
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


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def registered_users(request):
    context = dict()
    context['users'] = models.Profile.objects.all()
    return render(request, 'mainapp/chatroom.html', context)

@login_required
class AddTask(View):
    template_name = 'mainapp/add-new-task.html'
    form_class = forms.AddNewTask

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            task_form = form.save(commit=False)
            task_form.user = request.user
            task_form.save()
            return redirect('/')

        else:
            error = 'Something was wrong'
            return render(request, self.template_name, {'error': error})

@login_required
def task_collection(request):
    template_name = 'index.html'
    tasks = models.TechnicalTask.objects.all()
    return render(request, template_name, {'tasks': tasks})


# one simple task for discussion
# def simple_task(request, task_id):
#     template_name = 'mainapp/chatroom.html'
#     task = get_object_or_404(models.TechnicalTask, id=task_id)
#     return render(request, template_name, {'task': task})



@login_required
# adding reply to the task
def add_reply(request, task_id):
    template_name = 'mainapp/chatroom.html'
    form = forms.RepliesForm(request.POST, request.FILES)
    task = get_object_or_404(models.TechnicalTask, id=task_id)  # one task ---> for comments
    replies_collection = models.Replies.objects.filter(technical_task__id=task_id)

    if request.method == 'POST':
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.technical_task = get_object_or_404(models.TechnicalTask, id=task_id)
            if request.FILES:
                print(request.FILES.getlist('file'))
            reply.save()
            messages.success(request, 'Your comment was added successfuly!')
        return redirect('/')
    else:
        form = forms.RepliesForm()
        return render(request, template_name, {'form': form,
                                               'task': task,
                                               'replies_collection': replies_collection})



# class AddFile(View):
#     template_name = 'mainapp/add-new-task.html'
#     form_class = forms.FilesForm
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             fileform = form.save(commit=False)
#             fileform.user = models.Profile.objects.last()
#             fileform.save()
#             return render(request, self.template_name, {'form': form,
#                                                         'success': 'File was succesfuly added!'})
#
#         else:
#             error_message = 'Something is wrong with your data!'
#             return render(request, self.template_name, {'form': form,
#                                                         'eror_message': error_message})
