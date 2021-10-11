from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from .forms import MessageForm
from .models import Message


User = get_user_model()


def index(request):
    if not request.user.is_authenticated:
      return render(request, 'auth.html')
    incoming_msgs = Message.objects.filter(user=request.user)
    outgoing_msgs = Message.objects.filter(author=request.user)
    messages = [*outgoing_msgs, *incoming_msgs]
    
    result = set(msg.author for msg in messages)
    return render(
        request,
        'index.html',
        {
            'form': MessageForm(),
            'messages': result,
        }
    )


def get_user_messages(request, username):
    author = get_object_or_404(User, username=username)
    outgoing_msgs = Message.objects.filter(
        author=author,
        user=request.user,
    )
    incoming_msgs = Message.objects.filter(
        author=request.user,
        user=author,
    )
    messages = sorted(
        [*outgoing_msgs, *incoming_msgs],
        key=lambda msg: msg.pub_date
    )

    return render(
        request,
        'messages.html',
        {
            'messages': messages,
            'author': author,
        }
    )


def new_message(request):
    if request.method != 'POST':
        return redirect('index')
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.author = request.user
        message.save()

    return redirect('user-page', username=form.cleaned_data['user'])