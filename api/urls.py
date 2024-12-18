from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ArticleAPIView, 
    ArticleDetailAPIView, 
    CommentListCreateAPIView, 
    CommentDetailAPIView, 
    CustomTokenObtainPairView,
    get_csrf_token)




urlpatterns = [
    path("articles/", ArticleAPIView.as_view(), name="article_list"),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view(), name="article_detail"),
    path("articles/comments/", CommentListCreateAPIView.as_view(), name="comment_list_create"),
    path("articles/comments/<int:pk>/", CommentDetailAPIView.as_view(), name="comment_detail"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('custom-token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('csrf-token/', get_csrf_token, name='csrf_token'),

    


]
