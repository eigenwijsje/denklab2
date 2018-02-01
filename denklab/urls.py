from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('fragmente/', include('fragments.urls')),
    path('subscribers/', include('subscribers.urls')),
]
