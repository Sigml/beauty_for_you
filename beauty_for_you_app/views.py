from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, UpdateView, DetailView, ListView
from datetime import datetime

from .form import AddStaffForm, AddServiceForm, AddCategoryServiceForm, UserCreateForm, LoginForm, \
    AddCategoryShopForm, AddProductShopForm, UserUpdateForm, PasswordResetForm
from .models import Staff, Services, Category_service, Reservation, Product, Category_staff


def main(request):
    """
    View function for the main page of the application.
    Parameters:
        request (HttpRequest): An object representing the HTTP request.
    Returns:
        HttpResponse: An HTTP response containing the 'main.html' template with the 'category_service' context.
    """
    category_service = Category_service.objects.all()
    return render(request, 'main.html', {'category_service': category_service})


class StaffRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    """
    Mixin to check if the user is staff or has appropriate permissions.
    """

    def test_func(self):
        return self.request.user.is_staff


class StaffView(View):
    """
    The view for the 'staff' view retrieves and displays all data from the 'staff' model."
    """

    def get(self, request):
        staff = Staff.objects.all()
        return render(request, 'staff.html', {'staff': staff, })


class AddStaffListView(StaffRequiredMixin,CreateView):
    """
    The view for the 'staff' view allows for adding a new employee.
    """
    form_class = AddStaffForm
    template_name = 'form.html'
    success_url = '/staff'


class AddServiseCreateView(StaffRequiredMixin, CreateView):
    """
    The view for adding a new service.
    """
    form_class = AddServiceForm
    template_name = 'form.html'
    success_url = '/service'


class ServiceListView(View):
    """
    The view for the 'service' view retrieves and displays all data from the 'service' model."
    """
    def get(self, request):
        service = Services.objects.all()
        return render(request, 'service.html', {'service': service})


class AddCategoryServiceCreateView(StaffRequiredMixin, CreateView):
    """
    A view that allows staff users to add a new category service.
    """
    form_class = AddCategoryServiceForm
    template_name = 'form.html'
    success_url = '/category_service'


class CategoryServiceListView(View):
    """
    The view for the 'Category_service' view retrieves and displays all data from the 'Category_service' model."
    """
    def get(self, request):
        category = Category_service.objects.all()
        return render(request, 'category.html', {'category': category})


class UserCreateView(FormView):
    """
    A view that handles user registration and account creation.
    """
    form_class = UserCreateForm
    template_name = "regestration.html"
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        data.pop('password_confirmation')
        User.objects.create_user(**data)
        return super().form_valid(form)


class LoginView(View):
    """
    A view that handles user login functionality.
    """
    def get(self, request):
        form = LoginForm
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Użytkownik nie istnieje'

            return render(request, 'login.html', {'form': form, 'message': message})


class LogoutView(View):
    """
    A view that handles user logout functionality.
    """
    def get(self, request):
        logout(request)
        return redirect('/')


class ReservationCreateView(LoginRequiredMixin, View):
    """
    The view that handles the 'reservation' functionality and allows data to be saved to the database.
    """
    def get(self, request, category_service_id):
        user = request.user.username
        staff = Staff.objects.filter(category_staff__name=category_service_id)
        service = Services.objects.filter(category=category_service_id)
        category_service = Category_service.objects.filter(pk=category_service_id)
        all_times = ('07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',)
        context = {
            'user': user,
            "staff": staff,
            'service': service,
            'category_service': category_service,
            'all_times': all_times
        }
        return render(request, "reservation.html", context=context)

    def post(self, request, category_service_id):
        client = request.user
        category_service_name = request.POST.get('category_service')
        try:
            category_service = Category_service.objects.get(name=category_service_name)
        except Category_service.DoesNotExist:
            return render(request, 'reservation.html', {'error_message': 'Nie znaleziono kategorii o podanej nazwie'})
        staff = request.POST.get('staff')
        first_name, last_name = staff.split(" ")
        staff = Staff.objects.get(first_name=first_name, last_name=last_name)
        service = request.POST.get('service')
        service_obj = Services.objects.get(name=service)
        date = request.POST.get('date')
        time = request.POST.get('time')
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        if selected_date.weekday() >= 5:
            return render(request, 'reservation.html', {'error_message': 'Nie pracujemy w weekendy'})
        elif datetime.strptime(date, '%Y-%m-%d').date() < datetime.now().date():
            return render(request, 'reservation.html', {'error_message': 'data juz mineła'})
        else:
            reservation = Reservation.objects.create(client=client, staff=staff, date=date, time=time)
            reservation.service.set([service_obj])
            reservation.category_service.set([category_service])
        return render(request, "reservation.html", {'message': "Rezerwacja została przyjęta"})


class AddCategoryShopCreateView(StaffRequiredMixin, CreateView):
    """
    A view that allows staff users to add a new category shop.
    """
    form_class = AddCategoryShopForm
    template_name = 'form.html'
    success_url = "/"


class AddProductShopCreateView(StaffRequiredMixin, CreateView):
    """
    A view that allows staff users to add a new product in shop.
    """
    form_class = AddProductShopForm
    template_name = 'form.html'
    success_url = '/shop'


class ShopListView(View):
    """
    A view that displays a paginated list of products in the shop
    """
    def get(self, request):
        shop = Product.objects.all()
        paginator = Paginator(shop, 10)
        page = request.GET.get('page')
        product_shop = paginator.get_page(page)
        context = {
            'shop': product_shop
        }
        return render(request, 'shop.html', context=context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view that allows logged-in users to update their profile information.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'form.html'

    def get_success_url(self):
        return f'/user/detail/{self.object.pk}/'

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    A view that displays detailed information about a user's profile.
    """
    model = User
    template_name = 'user.html'
    context_object_name = 'user_obj'


class PasswordResetView(LoginRequiredMixin, FormView):
    """
    A view that allows authenticated users to reset their password.
    """
    form_class = PasswordResetForm
    template_name = 'form.html'
    success_url = '/'
    permission_required = 'auth.change_user'

    def form_valid(self, form):
        new_password = form.cleaned_data['password']
        user = self.request.user
        user.set_password(new_password)
        user.save()
        return super().form_valid(form)


class MyReservationView(LoginRequiredMixin, ListView):
    """
    A view that displays a list of reservations made by the authenticated user.
    """
    model = Reservation
    template_name = 'my_reservation.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        client = self.request.user
        queryset = Reservation.objects.filter(client=client)
        return queryset


class ServiceDeleteView(StaffRequiredMixin, DeleteView):
    """
    A view that allows staff users to delete a service
    """
    model = Services
    template_name = 'delete.html'
    success_url = '/service'


class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    """
    A view that allows staff users to update service.
    """
    model = Services
    fields = ('name', 'duration', 'price', 'category')
    template_name = 'form.html'
    success_url = '/service'


class CategoryServiceDeleteView(StaffRequiredMixin, DeleteView):
    """
    A view that allows staff users to delete a category service.
    """
    model = Category_service
    template_name = 'delete.html'
    success_url = '/category_service'


class StaffDeleteView(StaffRequiredMixin, DeleteView):
    """
     A view that allows staff users to delete a staff member
    """
    model = Staff
    template_name = 'delete.html'
    success_url = '/staff'


class AddStaffToCategoryView(StaffRequiredMixin, View):
    """
    A view that allows staff users to assign staff members to a category service.
    """

    def get(self, request):
        staff = Staff.objects.all()
        category_service = Category_service.objects.all()
        context = {
            'staff': staff,
            "category_service": category_service
        }
        return render(request, 'add_staff_to_category.html', context)

    def post(self, request):
        category_service = request.POST.get('category')
        staff = request.POST.get('staff')
        if category_service and staff:
            category_staff = Category_staff.objects.create()
            category_staff.name.set([category_service])
            category_staff.staff.set([staff])
            return render(request, 'add_staff_to_category.html', {'message': 'pracownik dodany'})
        else:
            return render(request, 'add_staff_to_category.html', {'message': 'Wystąpił błąd. Spróbuj ponownie.'})


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """
    A view that allows authenticated users to delete their reservation
    """
    model = Reservation
    template_name = 'delete.html'
    success_url = '/my_reservation'


class ReservationUpdateView(View):
    """
    A view that allows users to update their reservation
    """
    def get(self, request, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        all_times = ('07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',)
        return render(request, 'reservation_update.html', {'reservation': reservation, 'all_times': all_times})

    def post(self, request, reservation_id):
        date = request.POST.get('date')
        time = request.POST.get('time')
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        if selected_date.weekday() >= 5:
            return render(request, 'reservation_update.html', {'error_message': 'Nie pracujemy w weekendy'})
        elif datetime.strptime(date, '%Y-%m-%d').date() < datetime.now().date():
            return render(request, 'reservation_update.html', {'error_message': 'data juz mineła'})
        else:
            reservation = Reservation.objects.update(date=date, time=time)
        return redirect("my_reservation")


class StaffUpdateView(StaffRequiredMixin, UpdateView):
    """
    A view that allows staff users to update staff member information
    """
    model = Staff
    fields = ('first_name', 'last_name', 'phone', 'position', 'description')
    template_name = 'form.html'
    success_url = '/staff'


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    """
    A view that allows staff users to update product information
    """
    model = Product
    fields = ('name', 'description', 'price', 'categories')
    template_name = 'form.html'
    success_url = '/shop'


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    """
    A view that allows staff users to delete a product
    """
    model = Product
    template_name = 'delete.html'
    success_url = '/shop'
