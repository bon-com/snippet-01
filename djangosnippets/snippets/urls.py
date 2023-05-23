from django.urls import path, include
from . import views

urlpatterns = [
    path('new/', views.snippets_new, name='new'),
    path('<int:s_id>/', views.snippets_detail, name='detail'),
    path('<int:s_id>/edit/', views.snippets_edit, name='edit'),
    path('<int:s_id>/comments/new/', views.comment_snippet, name='comment'),
    path('<int:s_id>/delete/', views.snippets_delete, name='delete'),
    path('comments/delete/<int:c_id>/', views.delect_comment, name='delect_comment'),
    path('search/snippets/', views.search_snippets, name='search_snippets'),
]