from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet


app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('v1/posts', PostViewSet)
v1_router.register('v1/groups', GroupViewSet)
v1_router.register(r'^v1/posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register('v1/follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('', include(v1_router.urls)),
]
