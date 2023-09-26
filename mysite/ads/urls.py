from django.urls import path, reverse_lazy, re_path

from . import views
app_name = 'ads'

urlpatterns = [
    #path('', views.AdListView.as_view(), name='ad_list'), # I included the tag_view to that url, the next re_path is the upgraded one
    re_path(r'^(?:(?P<tag_name>[\w-]+)/)?$', views.AdListView.as_view(), name='ad_list'),
    path('create', views.AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),  # Fixed the typo in the view name
    path('<int:pk>/update', views.AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete', views.AdDeleteView.as_view(), name='ad_delete'),  # Moved the closing parenthesis to the correct place
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path('<int:pk>/comment',
        views.CommentCreateView.as_view(), name='ad_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads:ad_list')), name='ad_comment_delete'),
    path('ad/<int:pk>/favorite',
        views.fav_add, name='ad_favorite'),
    path('ad/<int:pk>/unfavorite',
        views.fav_remove, name='ad_unfavorite'),
    #path('<str:tag_name>', views.tag_view, name='tag_view') I gave up on this idea, I stick to DRY and will integrate the tag_view to the AdListView 
]
