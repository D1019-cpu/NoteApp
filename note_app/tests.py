from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # tạo user cho kiểm thử
        self.user = User.objects.create_user(username='testuser2002', password='@Testpassword2002')

    def testLogin(self):
        response = self.client.post(reverse('login'), {'username': 'testuser2002', 'password': '@Testpassword2002'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


    def testLogout(self):
        self.client.login(username='testuser2002', password='@Testpassword2002')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


    def testRegistration(self):
        response = self.client.post(reverse('register'), {'username': 'xuanhoantest1', 'email': 'xuanhoant111@gmail.com', 'password': '@Hoanktmt021', 'confirm-password': '@Hoanktmt021'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    

class NoteCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser22', password='@Test12342')
        self.note = Note.objects.create(user=self.user, content='# Hello World KTMT02')

    def testCreateNote(self):
        self.client.login(username='testuser22', password='@Test12342')
        response = self.client.post(reverse('create-note'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 2)  # kiểm tra xem Note mới đã được tạo chưa?
    
    def testUpdateNote(self):
        self.client.login(username='testuser22', password='@Test12342')
        response = self.client.post(reverse('save-note', args=[self.note.id]), {'content': 'Updated note content'})
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, 'Updated note content')

    def testDeleteNote(self):
        self.client.login(username='testuser22', password='@Test12342')
        response = self.client.post(reverse('delete-note', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)



# python manage.py test