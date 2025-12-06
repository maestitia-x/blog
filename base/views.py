from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category, Comment


# Create your views here.
def home(request):
    """Ana Sayfa - En Son 6 Blog Yazisi"""
    posts = Post.objects.filter(published=True)[:6]
    categories = Category.objects.all()
    context = {
        'posts':posts,
        'categories':categories
    }

    return render(request, 'base/home.html', context)

def posts(request):
    """Tum Blog Yazilari"""
    all_posts = Post.objects.filter(published=True)
    categories = Category.objects.all()

    context = {
        'posts':all_posts,
        'categories':categories
    }
    return render(request, 'base/posts.html', context)

def post(request, slug):
    """Tek bir blog yazisi detayi"""
    post_obj = get_object_or_404(Post, slug=slug, published=True)

    # Goruntulenme sayisini arttir
    post_obj.views += 1
    post_obj.save()

    # Yorumlari getir
    comments =post_obj.comments.filter(active=True)

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content: 
            Comment.objects.create(
                post = post_obj,
                author = request.user,
                content = content,
                active= True )
            messages.success(request, 'Yorumunuz basariyla kaydedildi')
            return redirect('post', slug=slug)
        else:
            messages.error(request, 'Yorum bos olamaz!')
    context={
        'post':post_obj,
        'comments':comments
    }
    return render(request, 'base/post.html', context)


def profile(request):
    """Kullanici profili"""
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author=request.user)
        user = request.user
        context = {
            'user_posts':user_posts,
            'user': user
        }
    else:
        context = {}
    return render(request, 'base/profile.html', context)

