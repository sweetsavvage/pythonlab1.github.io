from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Message
from .forms import UserMessageForm
from django.shortcuts import redirect

# Create your views here.
class Index(View):
    def get(self,request):
        users_list = User.objects.all()
        context = {
        'users_list':users_list,
        }
        return render(request,'Messanger/index.html',context=context)

class SendMessage(View):
    def get(self, request, id):
        if request.user.is_authenticated:
        # recipient_user = ''
            try:
                recipient_user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Http404

            message_form = UserMessageForm(initial={'author': request.user,'recipient':recipient_user})
            context = {
            'message_form':message_form,
            "recipient_name":recipient_user.username,
            }

            return render(request,'Messanger/send_message.html',context=context)
        else:
            return redirect('index')

    def post(self,request, id):
        if request.user.is_authenticated:
            message_form = UserMessageForm(request.POST or None)
            try:
                recipient_user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Http404
            if message_form.is_valid():
                if message_form.cleaned_data['author'].id != request.user.id or message_form.cleaned_data['recipient'].id != recipient_user.id:
                    raise Http404
                message_form.save()
                return redirect('index')
            else:
                print(message_form.errors)
        else:
            return redirect('index')

class MyMessages(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_messages = Message.objects.filter(recipient=request.user)
            send_messages = Message.objects.filter(author=request.user)
            context = {
                'get_messages':get_messages,
                'send_messages':send_messages,
            }
            return render(request,'Messanger/my_messages.html',context=context)
        else:
            return redirect('index')

class Admin(View):
    def get(self, request):
        if request.user.is_superuser:
            statistics = dict()
            for user in User.objects.all():
                statistics[user.username] = dict()
                distinct_recipients = list({mes.recipient for mes in Message.objects.filter(author=user)})
                for dr in distinct_recipients:
                    number = Message.objects.filter(author=user,recipient=dr).count()
                    statistics[user.username][dr]=number

            print(statistics)
            context = {
                'statistics':statistics
            }
            return render(request,'Messanger/admin.html',context=context)
        else:
            return redirect('index')

