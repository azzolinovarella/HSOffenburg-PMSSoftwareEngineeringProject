import unittest
from datetime import datetime
from json import dumps
from os import remove
from ..user_files.user import User
from ..password_files.password import Password as Psw
from .admin import Admin


class AdminTest(unittest.TestCase):

    def setUp(self):
        email = 'test1@gmail.com'
        password = 'Password1234'
        hspassword = Psw.gen_bcrypt(password)
        hibp = Psw.hibp(password)
        creation_date = str(datetime.now())
        self.user = User(email, hspassword, hibp, creation_date)

    def test_admin_checker(self):
        login = 'abc'
        pw1 = 'Pw1234'
        pw2 = 'Pw5678'
        hs_pw1 = Psw.gen_bcrypt(pw1)
        hs_pw2 = Psw.gen_bcrypt(pw2)
        rules = {"admin_login": login, "admin_hs_pw1": hs_pw1, "admin_hs_pw2": hs_pw2}  # We set the rules to check it
        with open('TestFile.json', 'w') as file:
            req = dumps(rules, indent=4)
            file.write(req)

        self.assertFalse(Admin.admin_checker('something', 'something', 'something', 'TestFile.json'))  # Wrong admin rules
        self.assertTrue(Admin.admin_checker(login, pw1, pw2, 'TestFile.json'))  # Correct admin rules

    def test_activate(self):
        self.assertTrue(self.user.active)
        for i in range(0, 10):
            self.user.get_user_data('wrong')  # To simulate someone trying to access a user data
        self.assertFalse(self.user.active)  # Now the user should be inactive
        Admin.activate(self.user)
        self.assertTrue(self.user.active)  # Now the user should be active

    def test_deactivate(self):
        self.assertTrue(self.user.active)  # Checking that the user is active
        Admin.deactivate(self.user)  # The admin process
        self.assertFalse(self.user.active)  # User should be inactive now

    def test_random_password(self):
        old_hs_pw = self.user._hspassword
        Admin.random_password(self.user)  # Here we change the user password to something random
        self.assertTrue(self.user._hspassword != old_hs_pw)

    def test_edit_admin_data(self):
        login = 'abc'
        pw1 = 'Pw1234'
        pw2 = 'Pw5678'
        hs_pw1 = Psw.gen_bcrypt(pw1)
        hs_pw2 = Psw.gen_bcrypt(pw2)
        rules = {"admin_login": login, "admin_hs_pw1": hs_pw1, "admin_hs_pw2": hs_pw2}  # Here we set the old rules
        with open('TestFile.json', 'w') as file:
            req = dumps(rules)
            file.write(req)
        self.assertTrue(Admin.admin_checker(login, pw1, pw2, 'TestFile.json'))  # Just to check if the file is ok
        new_login = 'def'
        new_pw1 = 'NewPassword'
        new_pw2 = 'NewPassword2'
        Admin.edit_admin_data(new_login, new_pw1, new_pw2, 'TestFile.json')  # Editing the rules
        self.assertFalse(Admin.admin_checker(login, pw1, pw2, 'TestFile.json'))  # Trying to access the admin with old admin data
        self.assertTrue(Admin.admin_checker(new_login, new_pw1, new_pw2, 'TestFile.json'))  # Now it's possible because this is the correct

    def tearDown(self):
        # Cleaning everything...
        try:
            remove('TestFile.json')
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
