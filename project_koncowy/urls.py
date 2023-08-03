"""
URL configuration for project_koncowy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from beauty_for_you_app.views import main, AddStaffListView, StaffView, AddCategoryServiceCreateView, \
    CategoryServiceListView, \
    AddServiseCreateView, ServiceListView, \
    CategoryServiceDeleteView, UserCreateView, LoginView, LogoutView, ReservationCreateView, ReservationCreateView_v2, \
    AddCategoryShopCreateView, AddProductShopCreateView, ShopListView, UserUpdateView, UserDetailView, \
    PasswordResetView, MyReservationView, ServiceDeleteView, StaffDeleteView, AddStaffToCategoryView, \
    ReservationDeleteView, ReservationUpdateView, StaffUpdateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='home'),
    path('add_staff/', AddStaffListView.as_view(), name='create_staff'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('add_category/', AddCategoryServiceCreateView.as_view()),
    path('category_service/', CategoryServiceListView.as_view()),
    path('add_service/', AddServiseCreateView.as_view()),
    path('service/', ServiceListView.as_view()),
    path('register/', UserCreateView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reservation/', ReservationCreateView.as_view()),
    path('reservation/<int:category_service_id>/', ReservationCreateView_v2.as_view(), name='reservation'),
    path('add_category_shop/', AddCategoryShopCreateView.as_view()),
    path('add_product_shop/', AddProductShopCreateView.as_view()),
    path('shop/', ShopListView.as_view()),
    path('user_update/', UserUpdateView.as_view()),
    path('user/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('my_reservation/', MyReservationView.as_view(), name='my_reservation'),
    path('delete_service/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),
    path('delete_category_service/<int:pk>/', CategoryServiceDeleteView.as_view(), name='delete_category_service'),
    path('delete_staff/<int:pk>/', StaffDeleteView.as_view(), name='delete_staff'),
    path('add_staff_to_category/', AddStaffToCategoryView.as_view()),
    path('delete_reservation/<int:pk>/', ReservationDeleteView.as_view(), name='delete_reservation'),
    path('update_reservation/<int:reservation_id>', ReservationUpdateView.as_view(), name='update_reservation'),
    path('update_staff/<int:pk>', StaffUpdateView.as_view()),
    path('shop_update_product/<int:pk>', ProductUpdateView.as_view()),
    path('shop_delete_product/<int:pk>', ProductDeleteView.as_view()),


]
