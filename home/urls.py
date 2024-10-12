from django.urls import path
from . import  views
app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delte/<int:post_id>', views.PostDeleteView.as_view(), name="delete", ),
    path('post/update/<int:post_id>', views.PostUpdateView.as_view(), name='post-update'),
    path('post/create/', views.PostCreateView.as_view(), name='post-crete'),
    path('reply/<int:post_id>/<int:comment_id>',views.AddReplyView.as_view(),name='reply'),
    path('like/<int:post_id>)',views.PostLikeView.as_view(),name='like'),

]
