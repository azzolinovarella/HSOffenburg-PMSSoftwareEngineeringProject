from json import dumps, load, decoder
from datetime import datetime
from re import match
from os import path
from ..password_files.password import Password as Psw


class User:

    def __init__(self, email, hspassword, hibp, creationdate, lastmodified=None, service_list=[],
                 warning=[False, 'Never', 0], active=True):
        """This is the constructor method and, so, here we define what the
         object from User may have."""

        self._email = email
        self._hspassword = hspassword
        self._hibp = hibp
        self._creationdate = creationdate
        self._lastmodified = lastmodified
        self._service_list = service_list
        self._warning = warning
        self._active = active

    def __repr__(self):
        """This method return us the object in a JSON format."""

        user_in_json = dumps(self.__dict__, indent=4)
        return user_in_json

    @property
    def active(self):
        """This method is used to check if a user is active or inactive."""

        return self._active

    @staticmethod
    def create_user(user_email, user_password):
        """This method creates a user for our system, but do not add its services
        (that should be added in another method after)."""

        validator = Psw.check_password(user_password)  # Check if the password is valid
        if validator is False:
            return 'Invalid password.'
        user_hs_psw = Psw.gen_bcrypt(user_password)
        user_hibp = Psw.hibp(user_password)
        new_user = User(user_email, user_hs_psw, user_hibp, str(datetime.now()))  # Create the user
        return new_user

    @staticmethod
    def user_to_json(users, file_path):
        """This method save all users object in a JSON file."""

        list_users_dict = [users[i].__dict__ for i in range(0, len(users))]  # Writing a list of dicts of users
        list_users_dict.sort(key=lambda dictionary: dictionary['_email'])  # Sorting the list by email
        with open(file_path, 'w') as file:
            for obj_dict in list_users_dict:
                ret = dumps(obj_dict, indent=4)
                file.write(ret)
        with open(file_path, 'r') as file:
            data = file.read()
            fixed_data = data.replace('}{', '},{')  # To fix the file to the right way (separing json's)
            fixed_data = f'[{fixed_data}]'  # To fix the file to the right way (putting every json together)
        with open(file_path, 'w') as file:
            file.write(fixed_data)  # Write the file in the right Json format

    @staticmethod
    def get_emails_and_users(file_path):
        """This method is used to get emails and users list in our system."""

        if path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    list_user_json = load(file)
            except decoder.JSONDecodeError:  # If we got this except, the file is corrupted
                list_user_json = []
        else:
            list_user_json = []  # If the file do not exists, we will generate an empty list of users
        user_emails = [list_user_json[i]['_email'] for i in range(0, len(list_user_json))]  # To become easier to validate if the user exists or not
        user_list = []
        for i in range(0, len(list_user_json)):
            user_list.append(User(*list_user_json[i].values()))  # Creating a list of User's instance in user_list
        return user_emails, user_list

    @staticmethod
    def check_email(email, email_list):
        """This method is used to check if a e-mail exists or if it's valid.
        If it exists, it returns the position where it is saved in the email list."""

        if not match(r"^[A-Za-z0-9\._\+-]+@[A-Za-z0-9\.-]+\.[a-zA-Z]*$", email):  # Validating the allowed characters
            return 'invalid', None
        elif email in email_list:
            pos = email_list.index(email)  # Here we get the position of the user in our system
            return 'exists', pos
        return 'do not exists', None

    def change_user_password(self, user_password, user_new_password):
        """This method allows the user to change its system's password."""

        if Psw.valid_password(user_password, self._hspassword):  # Verify if the password matches
            self._alert(False)  # Set alert False because the user's data is ok
            if Psw.check_password(user_new_password) is False:
                return 'Invalid', 'New password is invalid.'
            self._hspassword = Psw.gen_bcrypt(user_new_password)
            self._hibp = Psw.hibp(user_new_password)
            self._lastmodified = str(datetime.now())
            return 'Valid', 'Password changed successfully!'
        self._alert(True)  # Set alert True because there's a chance of somebody is trying to modify the user data
        return 'Invalid', 'Wrong password!'

    def create_service(self, user_password, service_name, service_password):
        """This method allows the user to add a service/application."""

        if Psw.valid_password(user_password, self._hspassword):  # Verify if the password matches
            self._alert(False)  # Set alert False because the user's data is ok
            all_services = self._service_list
            all_service_names = [all_services[i]["service_name"] for i in range(0, len(all_services))]
            if service_name not in all_service_names:
                service_hs_password = Psw.gen_bcrypt(service_password)
                service_hibp = Psw.hibp(service_password)
                all_services.append({"service_name": service_name, "service_hs_password": service_hs_password,
                                     "service_hibp": service_hibp, "service_creation_date": str(datetime.now()),
                                     "service_last_modified": None})  # Creating the service dict
                all_services.sort(key=lambda dictionary: dictionary["service_name"])
                return 'Valid', 'Service list added successfully!'
            return 'Invalid', 'This user already has a service with this name.'
        self._alert(True)
        return 'Invalid', 'Wrong password!'

    def change_service(self, user_password, service_name, service_new_password):
        """This method allows the user to change its service's password."""

        if Psw.valid_password(user_password, self._hspassword):  # Verify if the password matches
            self._alert(False)  # Set alert False because the user's data is ok
            all_services = self._service_list
            all_service_names = [all_services[i]["service_name"] for i in range(0, len(all_services))]
            if service_name in all_service_names:
                pos2 = all_service_names.index(service_name)
                service = self._service_list[pos2]
                service["service_hs_password"] = Psw.gen_bcrypt(service_new_password)
                service["service_hibp"] = Psw.hibp(service_new_password)
                service["service_last_modified"] = str(datetime.now())
                return 'Valid', 'Service password changed successfully!'
            return 'Invalid', 'This user do not have a service with this name.'
        self._alert(True)  # Set alert True because there's a chance of somebody is trying to modify the user data
        return 'Invalid', 'Wrong password!'

    def delete_service(self, user_password, service_name):
        """This method allows the user to delete a service."""

        if Psw.valid_password(user_password, self._hspassword):  # Verify if the password matches
            self._alert(False)  # Set alert False because the user's data is ok
            all_services = self._service_list
            all_service_names = [all_services[i]["service_name"] for i in range(0, len(all_services))]
            if service_name in all_service_names:
                pos2 = all_service_names.index(service_name)
                del self._service_list[pos2]
                return 'Valid', 'Service deleted successfully!'
            return 'Invalid', 'This user do not have a service with this name.'
        self._alert(True)  # Set alert True because there's a chance of somebody is trying to modify the user data
        return 'Invalid', 'Wrong password!'

    def get_user_data(self, user_password):
        """This method allows the user to get your data in JSON format."""

        if Psw.valid_password(user_password, self._hspassword):  # Verify if the password matches
            self._alert(False)  # Set alert False because the user's data is ok
            return 'Valid', self.__dict__
        self._alert(True)  # Set alert True because there's a chance of somebody is trying to modify the user data
        return 'Invalid', 'Wrong password!'

    def delete_user(self, user_password):  # Verify if the password matches
        """This method allows the user to delete your system's account."""
        if Psw.valid_password(user_password, self._hspassword):
            return 'Valid', 'User deleted successfully!'
        self._alert(True)  # Set alert True because there's a chance of somebody is trying to modify the user data
        return 'Invalid', 'Wrong password!'

    def _alert(self, mode):
        """This method change the variable warning if somebody tries to access/modify the user data.
        If it happes more than 10 times, it deactivate the user to protect it from hacker attacks."""

        if mode is True:
            self._warning[0] = True  # Saving that the last time they tried to access/modify the user data was unsuccessful
            self._warning[1] = str(datetime.now())  # Time when they tried (unsuccessfully) to access/modify the user data
            self._warning[2] += 1  # Used to control how many times the user typed its password wrong
            if self._warning[2] >= 10:
                self._active = False  # If we get 10 times in a row a wrong password, we deactivate the user
        else:
            self._warning[0] = False  # Saving that the last time they tried to acess/modify the user data was sucessful
            self._warning[2] = 0  # If the password typed is correct, we return the counter to 0

