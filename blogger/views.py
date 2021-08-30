from ckeditor_uploader.forms import SearchForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from taggit.models import Tag
from .forms import PostForm, CommentForm, EmailPostForm
from .models import Post, Category, Comment


# create blog post
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            t_str = title.lower()
            for i in range(0, len(t_str), 1):
                if t_str[i] == ' ':
                    t_str = t_str.replace(t_str[i], '-')
            obj = form.save(commit=False)
            obj.author = request.user
            obj.slug = t_str
            obj.save()
            form.save_m2m()
            return HttpResponseRedirect('/blogger/')
        else:
            print(form.errors)

    else:
        form = PostForm()
    return render(request, 'blogger/post/create.html', {'form': form})


# list blog posts
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    categories = Category.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogger/post/list.html', {
        'page': page,
        'posts': posts,
        'tag': tag,
        'categories': categories
    })


# blog post details
def post_detail(request, id, year, month, day, posts):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=id, slug=posts,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blogger/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'liked': liked,
        'categories': categories
    })


# edit blog post
@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    tag = post.tags.name
    print(tag)
    #post_form = PostForm(data=request.POST, files=request.FILES, instance=post)
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        post_image = request.FILES['post_image']
        '''
        post_form = Post(
            slug=post.slug,
            author=request.user,
            title=title,
            body=body,
            categories=post.categories,
            post_image=post_image
        )
        post_form.save()
        post.delete()
        '''
        post.title = title
        post.body = body
        post.post_image = post_image
        post.save()
        return HttpResponseRedirect('/blogger/')
    return render(request, 'blogger/post/edit_post.html', {'post': post, 'id': id})


@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blogger/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:  # check whether the form is submitted,
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            # search_vector = SearchVector('title', 'body', 'categories')
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B') + SearchVector('categories', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                              rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank') # filter(search=search_query)
    return render(request, 'blogger/post/search.html', {'form': form,
                                                         'query': query,
                                                         'results': results})


@login_required
def post_category(request, cats):
    category_posts = Post.objects.filter(categories=cats).order_by('-publish')
    return render(request, "blogger/post/category_post_list.html", {'cats': cats, 'category_posts': category_posts})


#@login_required
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-publish'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blogger/post/category_post_list.html", context)


def like_view(request, id, year, month, day, posts):
    liked = False

    if request.method == 'POST':
        post = get_object_or_404(Post, id=request.POST.get('post_id'),
                                 slug=posts,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

    return HttpResponseRedirect(reverse('blogger:post_detail', args=[int(id), int(year), int(month), int(day), str(posts)]))