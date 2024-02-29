from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ProteinsListView, ProteinsDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('protein_list/', ProteinsListView.as_view(), name='protein_list'),
    path('proteins/<int:pk>/', ProteinsDetailView.as_view(), name='protein_details'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('contact/', views.contact, name='contact'),
    path('overview/', views.overview, name='overview'),
    path('resources/', views.resources, name='resources'),
    path('cite/', views.cite, name='cite'),
    path('guide/', views.guide, name='guide'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)