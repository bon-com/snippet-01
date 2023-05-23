from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.test import TestCase
from .views import top, snippets_new, snippets_edit, snippets_detail
from django.urls import resolve
from django.contrib.auth import get_user_model
from .models import Snippet

UserModel = get_user_model()

class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = 'test_user',
            email = 'test@example.com',
            password = 'top_secret_pass001'
        )
        self.snippet = Snippet.objects.create(
            title = 'title',
            code = "print('Hello World')",
            description = 'description1',
            created_by = self.user
        )

    def test_should_return_snippet_title(self):
        req = RequestFactory().get("/")
        req.user = self.user
        res = top(req)
        self.assertContains(res, self.snippet.title)

    def test_should_return_username(self):
        req = RequestFactory().get("/")
        req.user = self.user
        res = top(req)
        self.assertContains(res, self.user.username)

# class TopPageViewTest(TestCase):
#     """ 一覧確認 """
#     def test_top_returns_200(self):
#         # req = HttpRequest() 直接view関数を呼び出す
#         res = self.client.get("/")
#         self.assertEqual(res.status_code, 200)

#     def test_top_returns_expected_content(self):
#         #req = HttpRequest()
#         #res = top(req)
#         res = self.client.get("/")
#         self.assertEqual(res.content, b'Hello World')

# トップページがb'Hello World'というプレーンテキストはなくHTMLファイルを返すように変更
# TopPageTestクラスを作成
class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        res = self.client.get('/')
        self.assertContains(res, 'Djangoスニペット')

    def test_top_page_uses_expected_telmlate(self):
        res = self.client.get('/')
        self.assertTemplateUsed(res, 'snippets/top.html')


class CreateSnippetsTest(TestCase):
    """ スニペットの新規登録確認 """
    # def test_should_resolve_new(self):
    #     found = resolve("/snippets/new")
    #     self.assertEqual(snippets_new, found.func)
    def setUp(self):
        self.user = UserModel.objects.create(
            username = 'test_user',
            email = '',
            password = 'secret'
        )
        self.client.force_login(self.user) # ユーザーログイン

    def test_render_creation_form(self):
        res = self.client.get('/snippets/new/')
        self.assertContains(res, 'スニペットの登録', status_code=200)

    def test_create_snippet(self):
        data = {'title': 'タイトル', 'code': 'コード', 'description': '解説'}
        self.client.post('/snippets/new/', data)
        snippet = Snippet.objects.get(title='タイトル')
        self.assertEqual('コード', snippet.code)
        self.assertEqual('解説', snippet.description)

# class DetailSnippetsTest(TestCase):
#     """ スニペットの詳細確認 """
#     def setUp(self):
#         self.user = UserModel.objects.create(
#             username = 'test_user',
#             email = 'test@example.com',
#             password = 'secret'
#         )
#         self.snippet = Snippet.objects.create(
#             title = 'タイトル',
#             code = 'コード',
#             description = '解説',
#             created_by = self.user
#         )

#     def test_should_use_expected_template(self):
#         url = f'/snippets/{self.snippet.id}/'
#         res = self.client.get(url)
#         self.assertTemplateUsed(res, '/snippets/snippet_detail.html')

#     def test_top_page_returns_200_and_expected_heading(self):
#         url = f'/snippets/{self.snippet.id}/'
#         res = self.client.get(url)
#         self.assertContains(res, self.snippet.title, status_code=200)
        

    # def test_should_resolve_detail(self):
    #     found = resolve("/snippets/1")
    #     self.assertEqual(snippets_detail, found.func)

class EditSnippetsTest(TestCase):
    """ スニペットの編集 """
    def test_should_resolve_edit(self):
        found = resolve('/snippets/1/edit')
        self.assertEqual(snippets_edit, found.func)

