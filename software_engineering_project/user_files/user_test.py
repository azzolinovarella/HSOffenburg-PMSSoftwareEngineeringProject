import unittest
from datetime import datetime
from os import path, remove
from json import load
from .user import User
from ..password_files.password import Password as Psw


class UserTest(unittest.TestCase):

    def setUp(self):
        self.emails = ['test1@gmail.com', 'test2@stud.hs-offenburg.de']
        self.passwords = ['Password1234', 'Password!@#$']
        hspasswords = [Psw.gen_bcrypt(self.passwords[0]), Psw.gen_bcrypt(self.passwords[1])]
        hibp = [Psw.hibp(self.passwords[0]), Psw.hibp(self.passwords[1])]
        creation_dates = [str(datetime.now()), str(datetime.now())]
        self.user0 = User(self.emails[0], hspasswords[0], hibp[0], creation_dates[0])
        self.user1 = User(self.emails[1], hspasswords[1], hibp[1], creation_dates[1])
        self.object_list = [self.user0, self.user1]

    def test_create_user(self):
        user_data = ['test@gmail.com', '1234']
        self.assertNotIsInstance(User.create_user(*user_data), User)  # Invalid password

        user_data[1] = 'Pass1234'
        self.assertIsInstance(User.create_user(*user_data), User)  # Password Ok --> now we can create the user

    def test_user_to_json(self):
        try:
            remove('FileTest.json')  # Just to make sure that we don't have this file
        except FileNotFoundError:
            pass

        self.assertFalse(path.exists('FileTest.json'))  # To show that the file was not here before

        User.user_to_json(self.object_list, 'FileTest.json')
        self.assertTrue(path.exists('FileTest.json'))  # To show that we created the file

        with open('FileTest.json') as file:
            load(file)  # If we got an error here, the file is not in JSON format
        remove('FileTest.json')

        self.assertFalse(path.exists('FileTest.json'))  # Just to check

    def test_get_email_and_users(self):
        User.user_to_json(self.object_list, 'FileTest.json')  # Supossing 'user_to_json' now is working, we can use it

        self.assertEqual(User.get_emails_and_users('AnotherFile.json'), ([], []))  # This should be empty (there's no 'AnotherFile.json')

        self.assertNotEqual(User.get_emails_and_users('FileTest.json'), ([], []))  # This should not be empty because we saved our users here

    def test_check_email(self):
        self.assertEqual(User.check_email('invalid2gmail.com', self.emails), ('invalid', None))

        self.assertEqual(User.check_email(self.emails[0], self.emails), ('exists', 0))  # 0 is the position of our user in our list

        self.assertEqual(User.check_email('valid@gmail.com', self.emails), ('do not exists', None))

    def test_change_user_password(self):
        self.assertEqual(self.user0.change_user_password('Something', 'Anything')[1],
                         'Wrong password!')  # 'Something' is not the correct old password

        self.assertEqual(self.user0.change_user_password(self.passwords[0], 'Anything')[1],
                         'New password is invalid.')  # 'Anything' is a non valid password

        self.assertEqual(self.user0.change_user_password(self.passwords[0], 'Pass1234')[1],
                         'Password changed successfully!')  # 'Pass1234' is a valid password

    def test_create_service(self):
        self.assertEqual(self.user0.create_service('Something', 'Instagram', '1234')[1],
                         'Wrong password!')  # 'Something' is not the correct password

        self.assertEqual(self.user0.create_service(self.passwords[0], 'Instagram', '1234')[1],
                         'Service list added successfully!')  # As we do not have a Instagram service, we can add it

        self.assertEqual(self.user0.create_service(self.passwords[0], 'Instagram', '1234')[1],
                         'This user already has a service with this name.')  # As we already have a Instagram service, we cannot add it

    def test_change_service(self):
        self.user0.create_service(self.passwords[0], 'Facebook', '1234')

        self.assertEqual(self.user0.change_service('Something', 'Google+', '1234')[1],
                         'Wrong password!')

        self.assertEqual(self.user0.change_service(self.passwords[0], 'Google+', '1234')[1],
                         'This user do not have a service with this name.')

        self.assertEqual(self.user0.change_service(self.passwords[0], 'Facebook', 'New1234')[1],
                         'Service password changed successfully!')

    def test_delete_service(self):
        self.user0.create_service(self.passwords[0], 'Gmail', '1234')

        self.assertEqual(self.user0.delete_service('Something', 'Hotmail')[1],
                         'Wrong password!')

        self.assertEqual(self.user0.delete_service(self.passwords[0], 'Hotmail')[1],
                         'This user do not have a service with this name.')

        self.assertEqual(self.user0.delete_service(self.passwords[0], 'Gmail')[1],
                         'Service deleted successfully!')

    def test_get_user_data(self):
        self.assertEqual(self.user0.get_user_data(self.passwords[0])[1],
                         self.user0.__dict__)  # The given data should be a dictionary with user data

        self.assertEqual(self.user0.get_user_data('1234')[1],
                         'Wrong password!')  # As the password is wrong, we cannot access it

    def test_delete_user(self):
        self.assertEqual(self.user0.delete_user('1234')[1],
                         'Wrong password!')

        self.assertEqual(self.user0.delete_user(self.passwords[0])[1],
                         'User deleted successfully!')

    def test__alert(self):
        self.assertEqual(self.user1._warning[2], 0)  # New user which we never tried to access it

        self.user1._alert(True)  # Setting alert to True --> somebody tried to access it
        self.assertEqual(self.user1._warning[2], 1)  # Should receive 1 because it means one wrong attempt

        self.user1._alert(True)  # Setting alert to True --> somebody tried to access it
        self.assertEqual(self.user1._warning[2], 2)  # Should receive 2 because it means two wrong attempts

        self.user1._alert(False)  # Setting alert to False --> it's ok, the user typed its password correctly
        self.assertEqual(self.user1._warning[2], 0)  # Should receive 0 because we set the counter to 0

    def tearDown(self):
        # Cleaning everything...
        pass


if __name__ == '__main__':
    unittest.main()

