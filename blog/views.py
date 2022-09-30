from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) 
#     page = request.GET.get('page')

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)

#     return render(request,  'blog/post/list.html', {'page':page, 'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                             status='published',
                              publish__year=year,
                                publish__month=month,
                                    publish__day=day)


    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post  = post

            # Save the comment to the database
            new_comment.save()
    comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# this class based view is analogous the function based view above
class PostListView(ListView):
    # queryset = Post.objects.all() # this can also be done by declaring model = Post. 
    model = Post
    context_object_name = 'posts' # default is object_list
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # retrive post from the database by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # This means form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"

            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ernestzottor@gmail.com.com', [cd['to']])
            sent = True
            # send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent':sent})


