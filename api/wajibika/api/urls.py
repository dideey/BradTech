"""Urls for the API endpoints
"""
from .serializers import *
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'leaders', views.LeadersViewSet)

"""
Nested routers for post under leaders
"""
leaders_router = NestedSimpleRouter(router, r'leaders', lookup='leader')
leaders_router.register(r'posts', views.PostViewSet, basename='leader-posts')

"""
Nested routers for comments under posts
"""

post_router = NestedSimpleRouter(leaders_router, r'posts', lookup='post')
post_router.register(r'comments', views.PostCommentViewSet, basename='post-comments')

urlpatterns = [
   path('signup/', views.SignupView.as_view(), name='signup'),
   path('login/', views.LoginView.as_view(), name='login'),
   path('logout/', views.Logout.as_view(), name='logout'),
   path('counties/', views.CountyView.as_view(), name='counties'),
   path('constituencies/', views.ConstituencyView.as_view(), name='constituencies'),
   path('wards/', views.WardView.as_view(), name='wards'),
   path('', include(router.urls)),
   path('', include(leaders_router.urls)),
    path('', include(post_router.urls)),
    #path('', include('rest_framework.urls'))
]