from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator

Position = (
    (1, 'kosmetyczka'),
    (2, 'masażystka'),
    (3, 'stylistka paznokci'),
    (4, 'fryzjer')
)


class Staff(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{1,10}$'), MinLengthValidator(9)])
    position = models.IntegerField(choices=Position)
    description = models.TextField(null=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def position_name(self):
        return Position[self.position - 1][1]


class Category_service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category_staff(models.Model):
    name = models.ManyToManyField(Category_service)
    staff = models.ManyToManyField(Staff)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField()
    category = models.ManyToManyField(Category_service)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    category_service = models.ManyToManyField(Category_service)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service = models.ManyToManyField(Services)
    date = models.DateField()
    time = models.TimeField(null=True)


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
