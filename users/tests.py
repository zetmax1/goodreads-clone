from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'yuta12345',
                'first_name': 'qwerty',
                'last_name': 'qwerty',
                'email': 'qwerty1@dmail.com',
                'password': '!2345678()'
            }
        )

        user = CustomUser.objects.get(username='yuta12345')

        self.assertEqual(user.username, 'yuta12345')
        self.assertEqual(user.first_name, 'qwerty')
        self.assertEqual(user.last_name, 'qwerty')
        self.assertEqual(user.email, 'qwerty1@dmail.com')
        self.assertNotEqual(user.password, '!2345678()')
        self.assertTrue(user.check_password('!2345678()'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'ali',
                'email': 'ali@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)

        self.assertFormError(response.context['form'], 'username', 'This field is required.')
        self.assertFormError(response.context['form'], 'password', 'This field is required.')

    def test_valid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'yuta12345',
                'first_name': 'qwerty',
                'last_name': 'qwerty',
                'email': 'qwerty1.com',
                'password': '!2345678()'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'yuta12345',
                'first_name': 'qwerty',
                'last_name': 'qwerty',
                'email': 'qwerty1@gmail.com',
                'password': '!2345678()'
            }
        )

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'yuta12345',
                'first_name': 'qwerty1',
                'last_name': 'qwerty1',
                'email': 'qwerty11@gmail.com',
                'password': '!234567118()'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):

    def setUp(self):
        self.db_user = CustomUser.objects.create(username='Ali', first_name="Aliyev", last_name='Valiyev')
        self.db_user.set_password('!2345678')
        self.db_user.save()

    def test_successfully_login(self):
        self.client.post(
           reverse('users:login'),
           data={
              'username':'Ali',
               'password': '!2345678'
           }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credential(self):
        self.client.post(
           reverse('users:login'),
           data={
              'username':'Ali-Wrong',
               'password': '!2345678'
           }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
           reverse('users:login'),
           data={
              'username':'Ali',
               'password': '!2345678-wrong'
           }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):

        self.client.login(username='Ali', password='!2345678')
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)

    def test_user_info(self):
        user = CustomUser.objects.create(username='aliy', first_name='Aliy', last_name='Abdullayev', email='ali@gmail.com')
        user.set_password('!2345678')
        user.save()

        self.client.login(username='aliy', password='!2345678')

        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.first_name)
        self.assertContains(response, user.username)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        self.assertEqual(response.status_code, 200)


    def test_update_user(self):
        user = CustomUser.objects.create(username='aliy', first_name='Aliy', last_name='Abdullayev', email='ali@gmail.com')
        user.set_password('!2345678')
        user.save()

        self.client.login(username='aliy', password='!2345678')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'Aliy1234',
                'first_name': 'Alibek',
                'last_name': 'Abdullayev',
                'email': 'ali1@gmail.com',
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.username, 'Aliy1234')
        self.assertEqual(user.first_name, 'Alibek')
        self.assertEqual(user.email, 'ali1@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))
