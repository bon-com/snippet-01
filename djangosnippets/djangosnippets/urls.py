from django.contrib import admin
from django.urls import path, include
from snippets.views import top

urlpatterns = [
    path('', top, name='top'),
    path('snippets/', include('snippets.urls')), # snippetsのurls.pyを参照
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
