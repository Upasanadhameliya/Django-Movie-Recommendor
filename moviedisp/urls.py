from django.urls import path
from . import views

urlpatterns = [
    path('<int:pageno>',views.home_page,name="home"),
    path('',views.home_page,name="home"),
    path('logout/',views.logout,name="Logout"),
    path('content/',views.content_based,name="content"),
    path('content/<int:pageno>',views.content_based,name="content"),
    path('related/',views.related,name="related"),
    path('related/<int:movie_id>',views.related,name="related")
]
