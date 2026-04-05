class ValidationError(Exception):
    def __init__(self, message):
        self.error = message

    def __str__(self):
        return self.error

    def __repr__(self):
        return self.error


class UserDataValidator:
    forbiddens = '!@#$%^&*=()[]{}\\/<>,%~?'
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__name_validate()
        self.__username_validate()
        self.__password_validate()


    def __name_validate(self):
        if hasattr(self, 'first_name') and hasattr(self, 'last_name') and hasattr(self, 'second_last_name'):
            if not self.second_last_name:
                pass
            else:
                if not self.second_last_name.isalpha():
                    raise ValidationError('Second last name have incorrect format.')

            for val in (self.first_name, self.last_name):
                if not val.isalpha():
                    raise ValidationError('First name or last name have incorrect format.')

                if not val.istitle():
                    raise ValidationError('First name or last name must start with a uppercase letter.')
        else:
            pass


    def __username_validate(self):
        if hasattr(self, 'user_name'):
            for c in self.user_name:
                if not c.isalnum() and c not in ('_', '.', '-'):
                    raise ValidationError('Username contains forbidden character.')
        else:
            pass


    def __password_validate(self):
        if hasattr(self, 'password') and hasattr(self, 'repeat_pass'):
            for p1, p2 in zip(self.password, self.repeat_pass):
                if p1 != p2:
                    raise ValidationError('Passwords do not match.')

                if p1 in self.forbiddens or p2 in self.forbiddens:
                    raise ValidationError('Password contain forbidden character.')
        else:
            pass



class PasswordValidator:
    forbiddens = '!@#$%^&*=()[]{}\\/<>,%~?'
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.__password_validate()


    def __password_validate(self):
        for p1, p2 in zip(self.password, self.repeat_pass):
            if p1 != p2:
                raise ValidationError('Passwords do not match.')

            if p1 in self.forbiddens or p2 in self.forbiddens:
                raise ValidationError('Password contain forbidden character.')




