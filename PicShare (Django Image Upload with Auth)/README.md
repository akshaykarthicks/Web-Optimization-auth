PicShare (Django Image Upload with Auth)

Overview
- Public home: image list (no login required)
- Protected action: upload image (login required)
- Auth: Django built‑in authentication (session-based, username/password)
- Media served locally during development

Requirements
- Python 3.12+
- Django 5.x
- Pillow

Install
```bash
pip install django pillow
```

Project structure (key parts)
```
picshare/
  manage.py
  picshare/
    settings.py
    urls.py
  iamge/
    urls.py
    views.py
    forms.py
    models.py
    templates/
      iamge/
        image_list.html   # public home
        upload.html       # requires login
        login.html        # login form
        register.html     # registration form
  media/                  # uploaded files (created at runtime)
```

Settings
- In `picshare/settings.py`:
  - `INSTALLED_APPS` includes `iamge`
  - Media:
    - `MEDIA_URL = '/media/'`
    - `MEDIA_ROOT = BASE_DIR / 'media'`
  - Templates: `APP_DIRS=True` and your app templates live under `iamge/templates/iamge/`
  - (Optional) Auth redirects:
    - `LOGIN_URL = 'login'`
    - `LOGIN_REDIRECT_URL = 'image_list'`

URLs
- `picshare/urls.py` (root):
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("iamge.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- `iamge/urls.py` (app):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),          # public home
    path('upload/', views.upload_image, name='upload_image'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
```

Models and Forms
- `iamge/models.py`
```python
from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

- `iamge/forms.py`
```python
from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']
```

Views (Auth flow and access control)
- Public: `image_list(request)` → renders all images (no decorator)
- Protected: `@login_required upload_image(request)` → saves new image via `ImageForm`
- Login: `login_view(request)` → authenticates with `authenticate()` and logs in with `auth_login()`
- Register: `register(request)` → creates user with `User.objects.create_user(...)`
- Logout: `logout_view(request)` → logs out and redirects to login

Important notes
- The login view function is named `login_view` to avoid shadowing `django.contrib.auth.login`.
- In login template, preserve redirect target:
```html
<input type="hidden" name="next" value="{{ request.GET.next }}">
```

Running locally
```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
# Visit http://127.0.0.1:8000/
```

Usage
1) Visit `/` to see public image list.
2) Click Upload → redirected to `/login/?next=/upload/` if not authenticated.
3) Log in (or go to `/register/` first). After login, redirected to `next` or the image list.
4) Upload images on `/upload/`. Files are stored under `media/images/`.

Troubleshooting
- TemplateDoesNotExist: ensure templates are under `iamge/templates/iamge/` and views use paths like `'iamge/upload.html'`.
- Broken images: confirm `MEDIA_URL`/`MEDIA_ROOT` and that `urlpatterns += static(...)` is present in `picshare/urls.py` while `DEBUG=True`.
- TypeError at /login: ensure URL routes use `views.login_view` and that auth import is aliased: `from django.contrib.auth import login as auth_login`.

Security (production)
- Serve media via web server (e.g., Nginx), not Django.
- Set `DEBUG=False`, configure `ALLOWED_HOSTS`, and secure session/cookie settings.


