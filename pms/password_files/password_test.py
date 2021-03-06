import unittest
from .password import Password as Psw


class PasswordTest(unittest.TestCase):

    def setUp(self):
        self.password1 = '123456789'
        self.password2 = 'Password'
        self.password3 = 'Password1234@'
        self.password4 = 'AV3r15tr0nGP4s5w0rD!@##@!$%'

    def test_check_password(self):
        # Using the password's rules set by default --> number of conditions = 4 and between 8 and 64
        self.assertEqual(Psw.check_password(self.password1), False)  # Number of conditions is lower than 4
        self.assertEqual(Psw.check_password(self.password2), False)  # Number of conditions is lower than 4
        self.assertEqual(Psw.check_password(self.password3), self.password3)  # Every condition satisfied
        self.assertEqual(Psw.check_password(self.password4), self.password4)  # Every condition satisfied

    def test_gen_sha1(self):
        # Using some previous known SHA1 (that is always the same) hashed passwords...
        self.assertEqual(Psw.gen_sha1(self.password3), 'a7eab432378cbd437bab745a6b0b83d5e6d13008')
        self.assertNotEqual(Psw.gen_sha1(self.password3), 'b566972ae7709eab297550cae362d5bee45c86d7')
        self.assertEqual(Psw.gen_sha1(self.password2), '8be3c943b1609fffbfc51aad666d0a04adf83c9d')
        self.assertNotEqual(Psw.gen_sha1(self.password2), '3eb8c943b1609fffbfc51aad666d0a04adf8d9c3')

    def test_valid_password(self):
        self.assertTrue(Psw.valid_password(self.password1, Psw.gen_bcrypt(self.password1)))  # Same passwords
        self.assertFalse(Psw.valid_password(self.password1, Psw.gen_bcrypt(self.password2)))  # Different passwords
        self.assertTrue(Psw.valid_password(self.password2, Psw.gen_bcrypt(self.password2)))  # Same passwords
        self.assertFalse(Psw.valid_password(self.password2, Psw.gen_bcrypt(self.password1)))  # Different passwords

    def test_hibp(self):
        # Using the password that had already been leaked (1,2 and 3) and one (4) that not yet (17/06/2020 - 15:56)
        self.assertTrue(Psw.hibp(self.password1)[0])
        self.assertTrue(Psw.hibp(self.password2)[0])
        self.assertTrue(Psw.hibp(self.password3)[0])
        self.assertFalse(Psw.hibp(self.password4)[0])

    def tearDown(self):
        # Cleaning everything...
        pass


if __name__ == '__main__':
    unittest.main()
