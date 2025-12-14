from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def home(request):
    """Ana Sayfa - En Son 6 Blog Yazisi"""
    posts = Post.objects.filter(published=True)
    categories = Category.objects.all()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'categories': categories,

    }

    return render(request, 'base/home.html', context)


def posts(request):
    """Tum Blog Yazilari"""
    all_posts = Post.objects.filter(published=True)
    categories = Category.objects.all()

    # Arama filtresi
    search_text = request.GET.get('search', '')
    if search_text:
        all_posts = all_posts.filter(Q(content__icontains=search_text) | Q(title__icontains=search_text))

    # Kategori filtresi
    category_id = request.GET.get('category', '')
    if category_id:
        all_posts = all_posts.filter(category_id=category_id)

    # PAGINATION - BURAYA YAZIN!
    # 1. Paginator oluştur (her sayfada 9 yazı)
    paginator = Paginator(object_list=all_posts, per_page=6)

    # 2. Sayfa numarasını al
    page_number = request.GET.get('page', 1)

    # 3. O sayfayı getir
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'categories': categories,
        'search_query': search_text,
        'selected_category': category_id
    }
    return render(request, 'base/posts.html', context)


def post(request, slug):
    """Tek bir blog yazisi detayi"""
    post_obj = get_object_or_404(Post, slug=slug, published=True)

    # Goruntulenme sayisini arttir
    post_obj.views += 1
    post_obj.save()

    # Yorumlari getir
    comments = post_obj.comments.filter(active=True)

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post_obj,
                author=request.user,
                content=content,
                active=True)
            messages.success(request, 'Yorumunuz basariyla kaydedildi')
            return redirect('post', slug=slug)
        else:
            messages.error(request, 'Yorum bos olamaz!')
    context = {
        'post': post_obj,
        'comments': comments
    }
    return render(request, 'base/post.html', context)


def profile(request):
    """Kullanici profili"""
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author=request.user)
        user = request.user
        context = {
            'user_posts': user_posts,
            'user': user
        }
    else:
        context = {}
    return render(request, 'base/profile.html', context)


def category(request, id):
    category_obj = get_object_or_404(Category, id=id)
    posts = category_obj.posts.filter(published=True)

    # paginator
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category_obj,
        'posts': page_obj,
        'all_posts': posts
    }
    return render(request, 'base/category.html', context=context)


def login_view(request):
    # Kullanıcı adı + şifre kontrol
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST )

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'{user.username} Basariyla giris yaptiniz!')
                return redirect('home')
            else:
                messages.error(request, 'There is no user!')
                return redirect('login')
    else:
        form = AuthenticationForm()
    # Eğer doğruysa → giriş yap
    # Değilse → hata mesajı

    context = {
        'form': form
    }
    return render(request, 'base/login.html', context)



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # Form doldurma
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Hos geldiniz {user.username}! Hesabiniz basariyla olusturuldu")
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'base/register.html', context)

    # Kullanıcı oluştur
    # Otomatik giriş yap
    pass


def logout_view(request):
    # Çıkış yap
    logout(request)
    # Ana sayfaya yönlendir
    messages.success(request, 'Basariyla cikis yaptiniz')
    return redirect('home')

