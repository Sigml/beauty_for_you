from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput

from .models import Staff, Services, Category_service, Reservation, Category, Product, Category_staff


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('first_name', 'last_name', 'phone', 'position', 'description')


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ('name', 'price', 'duration', 'category')



class AddCategoryServiceForm(forms.ModelForm):
    class Meta:
        model = Category_service
        fields = ('name',)
        widgets = {
            'name':forms.TextInput(attrs={
                'class': ' form-control',
                'placeholder': 'nazwa'
            })
        }


class UserCreateForm(forms.ModelForm):
    password_confirmation = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "hasło"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name')
        widgets = {

            'username': TextInput(attrs={
                'class': 'form-control',
                "placeholder": "username"
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                "placeholder": "email"

            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                "placeholder": "hasło"
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                "placeholder": "imię"
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                "placeholder": "nazwisko"
            })

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Podane hasła różnią się')

        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "username"}))

    password = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "hasło"}))


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time':forms.TimeInput(attrs={'type':'time'})
        }

class AddCategoryShopForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)


class AddProductShopForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'categories')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PasswordResetForm(forms.Form):
    password = forms.CharField(label="Haslo", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "hasło"}))
    password_confirmation = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "hasło"}))

    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirmation']:
            raise forms.ValidationError('Podane hasla roznia sie')


class AddStaffToCategoryForm(forms.ModelForm):
    class Meta:
        model = Category_staff
        fields = ('name', 'staff')
