from django.shortcuts import render
from django.db.models import Q 
from .models import Category, Info, Post, Author,IpModel
from django.views.generic import DetailView

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:4]
    context = {
        'post': post,
        'latest': latest,
    }
    return render(request, 'post.html', context)

def info (request):
    about = Info.objects.get()
    context = {
        'about':about
    }
    return render(request, 'user.html',context)
    

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip


class PostDetailViews(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'
    
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if IpModel.object.filter(ip=ip).exists():
            print("ip already present")
            post_id = request.GET.get('post-id')
            print(post_id)
            post = Post.objects.get(pk=post_id)
            post.views.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            post_id = request.GET.get('post_id')    
            post = Post.objects.get(pk=post_id)
            post.views.add(IpModel.objects.get(ip=ip))    
        return self.render_to_response(context)
