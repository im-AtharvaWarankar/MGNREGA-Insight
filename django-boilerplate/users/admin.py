# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Users
# Commented out imports for models not used in CivicView
# from .models import UsersDevices, ExportData


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        # 'firstName',  # Commented out - field not in model for CivicView
        # 'lastName',  # Commented out - field not in model for CivicView
        'email',
        # 'password',  # Don't display password in admin list
        # 'level',  # Commented out - field not in model for CivicView
        'is_active',
        'is_staff',
        'is_superuser',
        # 'isVerified',  # Commented out - field not in model for CivicView
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'is_active',
        'is_staff',
        'is_superuser',
        # 'isVerified'  # Commented out - field not in model for CivicView
    )
    raw_id_fields = ('groups', 'user_permissions')


# COMMENTED OUT — Admin for models not used in CivicView
# @admin.register(UsersDevices)
# class UsersDevicesAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'createdAt',
#         'updatedAt',
#         'userId',
#         'deviceId',
#         'token',
#         'deviceType',
#     )
#     list_filter = ('createdAt', 'updatedAt', 'userId')


# COMMENTED OUT — Admin for models not used in CivicView
# @admin.register(ExportData)
# class ExportDataAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'createdAt',
#         'updatedAt',
#         'userId',
#         'fileUrl',
#     )
