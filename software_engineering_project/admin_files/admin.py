from random import sample
from json import load, dumps
from datetime import datetime
from ..password_files.password import Password as Psw


class Admin:

    @staticmethod
    def admin_checker(admin, ver1, ver2, file_path):
        """This method checks if the admin_user data is correct or not."""

        with open(file_path, 'r') as file:
            admin_rules = load(file)  # Rever como salva as infos do arquivo!!

        if admin == admin_rules['admin_login']:
            hs1 = admin_rules['admin_hs_pw1']
            hs2 = admin_rules['admin_hs_pw2']
            if Psw.valid_password(ver1, hs1) and Psw.valid_password(ver2, hs2):
                return True
        return False

    @staticmethod
    def activate(user):
        """This method is used to activate an user."""

        user._alert(False)
        user._active = True
        return 'Valid', 'User activated.'

    @staticmethod
    def deactivate(user):
        """This method is used to deactivate an user."""

        user._alert(True)
        user._active = False
        user._warning[2] = 100  # To show that an admin deactivated it
        return 'Valid', 'User deactivated.'

    @staticmethod
    def delete(user):
        """This method is used to delete a user from our system."""

        if isinstance(user, object):
            del user
            return 'Valid', 'User deleted.'
        return 'Invalid', 'This is not an user.'

    @staticmethod
    def random_password(user):
        """This method is used to generate a random password for a user."""

        char = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?/.,:;'_-+="
        password = "".join(
            sample(char, 32))  # WE GENERATE A RANDOM PASSWORD TO ALLOW THE USER TO CHANGE IT LATTER
        hspassword = Psw.gen_bcrypt(password)
        user._hspassword = hspassword
        user._lastmodified = 'Edited by the admin in - ' + str(datetime.now())
        user._hibp = Psw.hibp(password)
        return 'Valid', f'The user {user._email} new password is {password} '

    @staticmethod
    def edit_admin_data(new_admin, new_ver1, new_ver2, file_path):
        """This method is used to edit all the admin data."""

        new_hs_ver1 = Psw.gen_bcrypt(new_ver1)
        new_hs_ver2 = Psw.gen_bcrypt(new_ver2)
        admin_data = {"admin_login": new_admin, "admin_hs_pw1": new_hs_ver1, "admin_hs_pw2": new_hs_ver2}
        with open(file_path, 'w') as file:
            ret = dumps(admin_data, indent=4)
            file.write(ret)

