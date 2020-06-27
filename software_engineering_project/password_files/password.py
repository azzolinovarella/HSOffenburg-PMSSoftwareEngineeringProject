from json import load
from requests import get
from hashlib import sha1
from os import path
from bcrypt import (hashpw, gensalt, checkpw)


class Password:

    @staticmethod
    def check_password(password):
        """Set a password according with many popular websites."""

        # As we want to work with the absolut path (because we need to call this method in different classes)
        # we will 'clean' this path and fix it to the right one (...password_files --> ...json_files).
        right_dir_path = path.dirname(__file__)
        right_dir_path = right_dir_path.rstrip('password_files') + 'json_files'

        with open(right_dir_path + '/PasswordEspecifications.json', 'r') as file:  # tirar .. depois
            req = load(file)
        numb_of_conditions = 0
        for i in range(0, len(password)):
            if password[i].isupper():
                req['IsUpper'] = True  # If the user has, at least, one upper character, we set it to True
            if password[i].islower():
                req['IsLower'] = True  # If the user has, at least, one lower character, we set it to True
            try:
                if int(password[i]) in list(range(0, 10)):
                    req['IsNumber'] = True  # If the user has, at least, one number character, we set it to True
            except ValueError:
                pass
            if password[i] in req['Special_possibilities']:
                req['IsSpecial'] = True  # If the user has, at least, one special character, we set it to True
            if password[i] not in req['Allowed_char']:
                return False  # If the user has a illegal character, we end this and don't allow its password
        for value in req.values():
            if value is True:
                numb_of_conditions += 1
        if numb_of_conditions >= 3 and 8 <= len(password) <= 64:
            return password  # If the number of conditions is 3 (or more) and the password is greater than 8 and lower than 64, we accept the password
        return False

    @staticmethod
    def gen_sha1(password):
        """Return your hashed password in SHA1."""

        return sha1(password.encode('utf-8')).hexdigest()

    @staticmethod
    def gen_bcrypt(password):
        """Return your hashed password in bcrypt with salt = 12."""

        password = str(hashpw(bytes(password, encoding='utf-8'), gensalt()))  # Converting binary type to string
        password = password[2:len(password) - 1]
        # We did this because the returned passowrd (converted from b->str) is something like b'PASSWORD' and we need
        # to clean that for something like PASSWORD
        return password

    @staticmethod
    def valid_password(password, hspassword):
        """Return True if the hashed password in bcrypt and the
        password matches or False if do not."""

        return checkpw(bytes(password, 'utf-8'), bytes(hspassword, 'utf-8'))

    @staticmethod
    def hibp(password):
        """Return a Tuple with True and the number of times that your password
         have been pwned or False and 0 if not."""

        pas_in_sha1 = Password.gen_sha1(password).upper()
        req = get('https://api.pwnedpasswords.com/range/' + pas_in_sha1[0:5])
        pas_list = req.text.split('\r')  # To separate every line of passwords
        pas_list = [pas_list[i].strip() for i in range(0, len(pas_list))]
        pas_verificator = pas_in_sha1[5::]  # To 'clean' the password to search for it in the list
        for element in pas_list:
            if element[0:35] == pas_verificator:
                return True, f'Pwned {element[36::]} time(s)'
        return False, 'Pwned 0 time(s)'

