from django.core.exceptions import ValidationError


def min_len_password(password):
    if len(password.strip()) < 8:
        raise ValidationError('Your password must be at least 8 characters long')


def char_check_password(password):
    if password.isalnum() == False:
        raise ValidationError('you can use just characters or numbers in your password')

def mobile_char_check(mobile):
    if mobile.isnumeric() == False or len(mobile) != 10:
        raise ValidationError('Wrong phone number!')

