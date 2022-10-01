from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


def share_post(request, post_id):
    post = get_object_or_404(Post,id=post_id, status='subscribed')

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data()
            subject = form_data['subject']
            email = form_data['email']
    else:
        form = EmailPostForm()

    return render(request, 'blog/share.html', {'form':form, 'post':post})
