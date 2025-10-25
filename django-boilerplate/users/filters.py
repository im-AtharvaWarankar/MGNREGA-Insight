from atomicloops.filters import AtomicDateFilter
from .models import Users
# Commented out - model not used in CivicView
# from .models import UsersDevices


class UsersFilter(AtomicDateFilter):
    class Meta:
        model = Users
        fields = (
            'createdAt',
            'updatedAt',
            'is_active',
            'is_superuser',
            'is_staff',
            # 'level'  # Commented out - field not in model for CivicView
        )


# COMMENTED OUT — Filter not used in CivicView
# class UsersDevicesFilter(AtomicDateFilter):
#     class Meta:
#         model = UsersDevices
#         fields = (
#             'createdAt',
#             'updatedAt',
#             'userId',
#         )
