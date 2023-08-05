from pymyorm.model import Model


class User(Model):
    tablename = 't_user'
    datetime_fields = ['time']
    decimal_fields = ['money']
