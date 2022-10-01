from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey


class StaffPermission(DjangoModelPermissions):
    pass


USER_PERMISSIONS = IsAuthenticated | HasAPIKey
