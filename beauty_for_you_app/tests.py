from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import date, time

from .models import Staff, Category_service, Services, Reservation
from .form import AddStaffForm, UserCreateForm

class TestStaffCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True
        self.user.save()

    def test_get(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create_staff')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddStaffForm)


    def test_post(self):
        create_staff = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '555555555',
            'position': 1,
            'description': 'descriptiondescription',
        }

        initial_staff_count = Staff.objects.count()

        response = self.client.post(reverse('create_staff'), data=create_staff)

        self.assertEqual(response.status_code, 302)

        new_staff = Staff.objects.last()

        self.assertEqual(Staff.objects.count(), initial_staff_count +1)

        self.assertIsNotNone(new_staff)
        self.assertEqual(new_staff.first_name, 'first_name')
        self.assertEqual(new_staff.last_name, 'last_name')
        self.assertEqual(new_staff.phone, '555555555')
        self.assertEqual(new_staff.position, 1)
        self.assertEqual(new_staff.description, 'descriptiondescription')


class TestUserCreate(TestCase):
    def test_get(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserCreateForm)

    def test_post(self):
        user_create = {
            'username': 'User',
            'first_name': 'name',
            'last_name': 'last_name',
            'email': 'email@email.com',
            'password': 'dddd!!22231',
            'password_confirmation': 'dddd!!22231',
        }

        initial_user_count = User.objects.count()

        response = self.client.post(reverse("register"), data=user_create)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.count(), initial_user_count + 1)

        new_user = User.objects.last()
        self.assertEqual(new_user.username, 'User')
        self.assertEqual(new_user.first_name, 'name')
        self.assertEqual(new_user.last_name, 'last_name')
        self.assertEqual(new_user.email, 'email@email.com')
        self.assertTrue(new_user.check_password('dddd!!22231'))


class TestReservation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.employee = Staff.objects.create(first_name='John', last_name='Doe', phone='123456789', position=1)
        self.service = Services.objects.create(name='Test Service', price=10.0, duration=60)
        self.today = date.today()
        self.category_service = Category_service.objects.create(name='Test Category')

        self.reservation = Reservation.objects.create(
            client=self.user,
            staff=self.employee,
            date=self.today,
            time=time(14, 0)
        )

        self.reservation.service.add(self.service)
        self.reservation.category_service.set([self.category_service])

    def test_get(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('reservation', args=[self.category_service.pk])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertIn('user', response.context)
        self.assertIn('staff', response.context)
        self.assertIn('service', response.context)
        self.assertIn('all_times', response.context)

    def test_post(self):
        url = reverse('reservation', args=[self.category_service.pk])
        data = {
            'client': self.user.pk,
            'staff': self.employee.pk,
            'service': self.service.pk,
            'date': self.today,
            'time': time(14, 0)
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code,
                         302)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.client, self.user)
        self.assertEqual(reservation.staff, self.employee)
        self.assertEqual(reservation.date, self.today)
        self.assertEqual(reservation.time, time(14, 0))
        self.assertIn(self.service, reservation.service.all())
        self.assertIn(self.category_service, reservation.category_service.all())

class ServiceUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True
        self.user.save()

        self.category = Category_service.objects.create(name='Testowa kategoria')
        self.service = Services.objects.create(name='Testowa usługa', price=100, duration=60)
        self.service.category.add(self.category)


        self.url = reverse('service_update', kwargs={'pk': self.service.pk})

    def test_service_update(self):
        self.client.login(username='testuser', password='testpassword')

        updated_data = {
            'name': 'Zaktualizowana usługa',
            'price': 150,
            'duration': 90,
            'category': [self.category.pk],
        }

        response = self.client.post(self.url, data=updated_data)

        self.assertEqual(response.status_code, 302)
        expected_url = reverse('service_list')

        updated_service = Services.objects.get(pk=self.service.pk)

        self.assertEqual(updated_service.name, updated_data['name'])
        self.assertEqual(updated_service.price, updated_data['price'])
        self.assertEqual(updated_service.duration, updated_data['duration'])
        self.assertListEqual(list(updated_service.category.all()), [self.category])
