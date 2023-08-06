
from re import fullmatch

from generallibrary import BoolStr, AutoInitBases

class _GeneralShared(metaclass=AutoInitBases):
    """ Subclassed by GeneralServer & GeneralClient. """
    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not fullmatch(regex, email):
            return BoolStr(False, "Invalid email")
        return BoolStr(True, "Valid email")

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return BoolStr(False, "Password has to be at least 8 characters.")
        return BoolStr(True, "Valid password")

