class UserSerializerFields:
    BASE = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups', 'created', 'updated']
    READ_ONLY = ['subscription']
    CREATION = BASE + ['repeat_password']
