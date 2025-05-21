from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTests(TestCase):

    def test_signup_view(self):
        """アカウント登録ページにアクセスできるかテスト"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/register.html')

    def test_successful_signup(self):
        """アカウント登録が正常に行われるかテスト"""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com'
        })
        
        # バリデーションエラーが発生した場合、エラーメッセージを出力
        if response.status_code == 200:
            print("Validation errors:", response.context['form'].errors)
        
        # 成功時にリダイレクトすることを確認
        self.assertRedirects(response, reverse('registration_success'))
        
        # ユーザーが作成されたか確認
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        """ログインページにアクセスできるかテスト"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/login.html')

    def test_successful_login(self):
        """ログインが正常に行われるかテスト"""
        # テスト用ユーザーを作成
        User.objects.create_user(username='testuser', password='testpassword123')
        # ログインリクエスト
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # ログイン後のリダイレクトを確認
        self.assertRedirects(response, reverse('main_page'))

    def test_logout(self):
        """ログアウトが正常に行われるかテスト"""
        # テスト用ユーザーを作成してログイン
        User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        # ログアウトリクエスト
        response = self.client.get(reverse('logout'))
        # ログアウト後のリダイレクトを確認
        self.assertRedirects(response, reverse('home'))
