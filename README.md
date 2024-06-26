# Step memulai django
1. membuat project `django-admin startproject namaproject . `
2. membuat app
   1. satu project dapat memiliki banyak app
   2. buat app di dalam folder project `python manage.py startapp nama_apps`
3. buat index di views dengan argument request
4. buat file urls di app, import views
5. add variabel app_name dan urlpatterns di apps.
6. tambahkan apps. di settings
7. jalankan server `python manage.py runserver`

# pembuatan template
1. buat folder templates/nama_apps di apps
2. isilah file jinja html
3. bisa set global templates di settings.py DIR => BASE_DIR / nama_folder

# migrasi db
1. `python manage.py migrate` untuk melakukan migrasi db
2. membuat migrasi app `python manage.py makemigrations nama_app`

# django shell
1. membuka shell `python manage.py shell`
2. beberapa query
   ```python
      #  select all
      from foodie_app.models import Category
      categories = Category.objects.all()
      categories
      <QuerySet []>
      
      ###create
      cat = Category.objects.create(name="Ali")
      categories
      <QuerySet [<Category: Ali>]>
      
      
      ```
3. membuat super user `python manage.py createsuperuser
4. register model yang di buat di file admin `admin.site.register(nama_class_model)` agar bisa dilihat lewat admin
5. menampilkan kolom di django admin `
   class  CategoryAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'date_added')
   admin.site.register(Category, CategoryAdmin)`


## query set (get data from database)
1. get all
    `recipes = Recipe.objects.all()`
2. get first
   `recipes = Recipe.objects.first()`
3. get by some_field
   `recipes = Recipe.objects.get(id=2)`
4. filter by category name (any foreign key)
   `recipes = Recipe.objects.filter(category__name__exact="Makanan Tradisional")`
   case insensitive
   `recipes = Recipe.objects.filter(category__name__iexact="Makanan Tradisional")`
   contains
   `recipes = Recipe.objects.filter(category__name__icontains="masakan")`
5. exclude
   `recipes = Recipe.objects.exclude(name="Nasi Goreng")`
6. filter chaining (use - to descending)
   `recipes = Recipe.objects.filter(category__name='Masakan Tradisional').order_by('-date_added')`
7. slice and aggregating
   contoh slice
   `recipes = Recipe.objects.all().order_by('-date_added')[:1]`
   aggregasi
   `from django.db.models import Avg, Count, Max`
   ` recipes = Recipe.objects.aggregate(Count('id'))`
8.  selengkapnya dapat dilihat di django queryset API
9.  menggunakan Q object untuk query yang lebih kompleks
    `from django.db.models import Q`
    `recipes = Recipe.objects.filter(Q(name__startswith='C') | Q(description__contains='cokelat'))`
10. mendapatkan return dictionary dengan menambahkan values()
    `recipes = Recipe.objects.filter(Q(name__startswith='E') | Q(description__contains='cokelat')).values()`
    jika ingin return list ganti values jadi values_list()
    untuk jumlah data count()
    mengecek apakah ada dengan exists()

## template
1. `{% url "nama_modul:nama_url" recipe.id %}`
2. meta class di dalam class model bisa untuk order data seperti ini ataupun penamaan dalam django admin
   `
   class Category(models.Model):
    
    name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["-name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
   `
3. class based view
   1. pada view import ListView dari django.views.generic
   2. defenisikan class dengan inherit dari listview
   `class RecipeListView(ListView):
    model = Recipe
    template_name = 'sandbox/index.html'
    context_object_name = 'recipes'
    ordering = ['date_added']
    `
   3. pada bagian url, import class tersebut dan panggil dengan as view
   ` path('recipes/', views.RecipeListView.as_view())`
   4. untuk detail view sama juga import DetailView, pada bagian url yang jadi id adalah pk `<int:pk>`
   5. object_list adalah default dari context_object_name jika tidak ada
   6. untuk melakukan filtering dengan class based view dapat dengan membuat fungsi yang diawali dengan get_dst
   `
   def get_queryset(self):
        recipe = Recipe.objects.filter(name__icontains='makanan')
        return recipe
   `
4. jika ingin custom class based view import saja View 

## pembuatan form
1. buat forms.py
2. from django.forms import Form
3. kemudian buat class Form dan meta didalamnya
   `
   class CategoryForm(Form):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Category Name'
        }
   `
4. import class form tersebut di view
5. Form terlalu general maka gunakan ModelForm
6. tambahkan {% csrf_token %} pada form
7. pada method post => form = CategoryForm(request.POST) agar dapat dilakukan pengecekan apakah valid? kalau ya dapat di save
   `
   if form.is_valid():
            form.save()
            return redirect('foodie_app:index')
   `
8. create data => ModelClass.objects.create(**kwargs) jika tidak menggunakan model ModelForm
9. dapat menambahkan widget pada form

## Auth
1. include untuk memanggil di tempat lain
   `path('', include('django.contrib.auth.urls'))`
2. untuk membuat form register dan login
   `
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib.auth import login

   def register(request):
    
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()            
            login(request, new_user)
            return HttpResponse('register')
        
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

   `
3. mengecek apakah user sudah login `{% if user.is_authenticated %}`
4. pada settings project
   LOGIN_REDIRECT_URL = 'foodie_app:index'
   LOGOUT_REDIRECT_URL = 'foodie_app:index'
   LOGIN_URL = 'accounts:login'

## install bootstrap di django
1. `pip install django-bootstrap5`
2. tambahkan ke project settings `django_bootstrap5`
3. `{% load django_bootstrap5 %}` pada template
4. tambahkan pada base.html
   `{% bootstrap_css %}
    {% bootstrap_javascript %
    `
5. contoh pemanggilan pada form
   `
   {% extends "base.html" %}
   {% load django_bootstrap5 %}
   {% block page_header %}
    <h2>Add a new Recipe</h2>
    {% if category %}to {{ category.name }}{% endif %}
   {% endblock page_header %}
   {% block content %}
   <div class="container">
      <form method="post">
         {% csrf_token %}
         {% bootstrap_form form %}
         {% bootstrap_button button_type="submit" content="Save Recipe" %}
      </form>
   </div>
   {% endblock content %}
   `
## membuat user profile
1. siapkan kode seperti ini di folder accounts pada models.py
   ```
   from django.db import models
   from django.contrib.auth.models import User
   from django.dispatch import receiver
   from django.db.models.signals import post_save 

   class UserProfile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
      bio = models.TextField(blank=True, null=True)
      date_created = models.DateTimeField(auto_now_add=True)
      profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
      
      def __str__(self):
         return self.user.username
      
      @receiver(post_save, sender=User)
      def create_or_update_user_profile(sender, instance, created, **kwargs):
         if created:
               UserProfile.objects.create(user=instance)
         instance.profile.save()
   ```
2. setiap kali objek User disimpan (baik dibuat atau diperbarui), fungsi create_or_update_user_profile akan dipanggil.
3. Sinyal adalah cara untuk memungkinkan komponen berbeda dari aplikasi berkomunikasi ketika tindakan tertentu terjadi. sinyal digunakan untuk memberitahu bagian lain dari aplikasi bahwa sesuatu telah terjadi
4. Receiver adalah fungsi yang dijalankan ketika sinyal diterima, ekorator @receiver digunakan untuk menghubungkan fungsi receiver dengan sinyal tertentu.
5. created: Boolean yang menunjukkan apakah instance baru dibuat (True) atau diperbarui (False)
6. pembuatan form dan view, image_field.url => memanggil lokasi url
7. ```
      class UserProfileForm(forms.ModelForm):
         class Meta:
            model = UserProfile
            fields = ['bio', 'profile_photo']
   ```

   ```
   def edit_user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse('Profile was updated successfully')
    else:
        form = UserProfileForm(instance=request.user.profile)    
    
    return render(request, 'registration/edit_profile.html', context={'form': form})
   ```
8. Models.objects.get_or_create() => check apa ada, jika tidak maka create
9. pada settings di project tambahkan variabel untuk foto
    `
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    `
10. pada project url ditambahkan juga path berikut
    from django.conf.urls.static import static
    from foodie import settings
    ##### concat url pattern dengan ini
    `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
11. decorator untuk verifikasi akses khusus untuk yang login saja `from django.contrib.auth.decorators import login_required` jika tidak maka akan di direct langsung ke LOGIN_URL 

## messaging
1. from django.contrib import messages
2.  messages.add_message(request, messages.SUCCESS, 'Feedback send successfully!')
3.  pada bagian view tambahkan kode diatas
4.  pada bagian template tambahkan berikut
   `
   {% if messages %}
    <div class="messages">
        {% for message in messages %}
            <p class="{{ message.tags }}">{{ message }}</p>
        {% endfor %}
    </div>
   {% endif %}
   `
5. dapat menambahkan context processor sendiri seperti search form pada settings TEMPLATES - context_processor 


## REST
1. install django_rest_framework
2. buat serializer
   ```
   class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients', 'directions', 'category', 'date_added', 'user', 'image', 'favorited_by']
        read_only_fields = ['image']
   ```
3. add rest_framework di setting
4. buat viewset di view
   ```
   class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
   ```
5. di url tambahkan berikut
   ```
   router = DefaultRouter()
   router.register(r'recipes', views.RecipeViewSet, basename='recipes')
   ```
6. dibagian urlpatterns tambahkan hal berikt
   ```
   path('api/', include(router.urls)),
   ```
7. untuk melihat api di http://127.0.0.1:8000/recipes/api/recipes/?format=api
   
## Heroku
1. buat file procfile `web: gunicorn nama_project.wsgi`
2. install library gunicorn dan whitenoise, tambahkan middleware whitenoise
3. buat static folder untuk static root
4. python manage.py collectstatic => mengumpulkan static
5. freeze requirements library to txt