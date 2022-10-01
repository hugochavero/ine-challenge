class UserSerializerConstants:
    BASE = [
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'groups',
        'subscription',
        'created',
        'updated'
        ]
    READ_ONLY = ['id', 'username', 'subscription', 'created', 'updated']
    SMALL_READ_ONLY = ['id', 'username', 'first_name', 'last_name']
    CREATION = BASE + ['repeat_password']

    PASSWORD_MASK = '******'


class SubscriptionConstants:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ERROR = 'error'

    CHOICES = [
        (ACTIVE, "Activa"),
        (INACTIVE, "Inactiva"),
        (ERROR, "Error")
    ]


class PasswordValidationConstants:
    REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    MESSAGE = {
        "password": "Password must include lowercase and upercase letters, digits and symbols and At least 8 characters"
    }
