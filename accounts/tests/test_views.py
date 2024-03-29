from django.test import TestCase
import accounts.views
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'user@example.com'
        })
        self.assertRedirects(response, '/')


    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'user@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for ToDoLists')
        self.assertEqual(from_email, 'i.popov@helpist.ru')
        self.assertEqual(to_list, ['user@example.com'])

#     def test_sends_mail_to_address_from_post(self):
#   '''I leave this here as an example of how we can mock 
#      functions manually, without using the Mock module.
#   '''
#             self.send_mail_called = False
# 
#             def fake_send_mail(subject, body, from_email, to_list):
#                 self.send_mail_called = True
#                 self.subject = subject
#                 self.body = body
#                 self.from_email = from_email
#                 self.to_list = to_list
# 
#             accounts.views.send_mail = fake_send_mail
# 
#             self.client.post('/accounts/send_login_email', data={
#                 'email': 'user@example.com'
#             })
# 
# 
#             self.assertTrue(self.send_mail_called)
#             self.assertEqual(self.subject, 'Your login link for ToDoLists')
#             self.assertEqual(self.from_email, 'noreply@todolists')
#             self.assertEqual(self.to_list, ['user@example.com'])
#

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'user@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Please, check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")


    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email', data={
            'email': 'user@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'user@example.com')


    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'user@example.com'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')  
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')


    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):  
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,  
            call(uid='abcd123')  
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)

