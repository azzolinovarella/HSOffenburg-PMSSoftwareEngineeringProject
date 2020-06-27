import unittest
from json import dumps
from .app import app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        resp_get = self.app.get('/')

        self.assertEqual(resp_get.status_code, 200), 'We should receive an OK (200).'

    def test_add_user(self):
        resp_post = self.app.post('/add_user',
                                  data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234'}),
                                  content_type='application/json')

        self.assertEqual(resp_post.status_code, 200), 'We should receive an OK (200).'

    def test_edit_password(self):
        resp_put = self.app.put('/edit_password',
                                data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234',
                                            'user_new_password': 'Pasword123456789'}),
                                content_type='application/json')

        self.assertEqual(resp_put.status_code, 200), 'We should receive an OK (200).'

    def test_add_service(self):
        resp_put = self.app.put('/add_service',
                                data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234',
                                            'service_name': 'Facebook', 'service_password': 'FacebookPassword'}),
                                content_type='application/json')

        self.assertEqual(resp_put.status_code, 200), 'We should receive an OK (200).'

    def test_edit_service(self):
        resp_put = self.app.put('/edit_service',
                                data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234',
                                            'service_name': 'Facebook', 'service_password': 'FacebookPassword',
                                            'service_new_password': 'FacebookNewPassword'}),
                                content_type='application/json')

        self.assertEqual(resp_put.status_code, 200), 'We should receive an OK (200).'

    def test_del_service(self):
        resp_delete = self.app.delete('/del_service',
                                      data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234',
                                                  'service_name': 'Facebook',
                                                  'service_password': 'FacebookNewPassword'}),
                                      content_type='application/json')

        self.assertEqual(resp_delete.status_code, 200), 'We should receive an OK (200).'

    def test_check_user(self):
        resp_get = self.app.get('/check_user',
                                data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234',
                                            'service_name': 'Facebook', 'service_password': 'FacebookPassword',
                                            'service_new_password': 'FacebookNewPassword1234'}),
                                content_type='application/json')

        self.assertEqual(resp_get.status_code, 200), 'We should receive an OK (200).'

    def test_del_user(self):
        resp_delete = self.app.delete('/del_user',
                                      data=dumps({'user_email': 'test@gmail.com', 'user_password': 'Password1234'}),
                                      content_type='application/json')

        self.assertEqual(resp_delete.status_code, 200), 'We should receive an OK (200).'

    def test_admin_options(self):
        resp_admin_opt = self.app.put('/admin_options',
                                      data=dumps({'admin_login': 'admin@admin', 'admin_pw1': 'Something',
                                                  'admin_pw2': 'Something', 'admin_opt': 'OPT0',
                                                  'user_email': 'test@gmail.com'}),
                                      content_type='application/json')

        self.assertEqual(resp_admin_opt.status_code, 200), 'We should receive an OK (200).'

    def test_admin_edit(self):
        resp_admin_edit = self.app.put('/admin_edit',
                                       data=dumps({'admin_login': 'admin@admin', 'admin_pw1': 'Something',
                                                   'admin_pw2': 'Something', 'admin_new_login': 'new_admin@admin',
                                                   'admin_new_pw1': 'Something', 'admin_new_pw2': 'Something'}),
                                       content_type='application/json')

        self.assertEqual(resp_admin_edit.status_code, 200), 'We should receive an OK (200).'

    def tearDown(self):
        # Cleaning everything...
        pass


if __name__ == '__main__':
    unittest.main()
