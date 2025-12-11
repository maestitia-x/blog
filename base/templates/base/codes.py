def posts(request):
    """Tum Blog Yazilari"""


all_posts = Post.objects.filter(published=True)
categories = Category.objects.all()
# BURADAN BAŞLAYIN - Arama mantığını ekleyin
# \TODO: 1. Arama kelimesini al (request.GET.get...)
#  \search_key = request.GET.get('search','')
# TODO: 2. Eğer arama kelimesi varsa (if ...)
#  if search_key:     # TODO: 3. Veritabanında ara (Q objects kullan)
#   all_posts = Post.objects.filter(
#   Q(title__icontains=search_key) | Q(content__icontains=search_key)         )     context = {         'posts':all_posts,         'categories':categories     }
#   #arama kelimesini context e ekleyin
#   return render(request, 'base/posts.html', context)
