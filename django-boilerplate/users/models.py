from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from atomicloops.models import AtomicBaseModel
from django.utils.translation import gettext_lazy as _


# User Manager
# User Manager
class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # Removed level field setting - not needed for CivicView

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self.create_user(email, password, **extra_fields)


# COMMENTED OUT — unused for CivicView
# USER_CHOICES = (
#     (5, 5),  # Admin
#     (1, 1),  # Trainee
#     (2, 2),  # Organization Users
# )


class Users(AbstractUser, AtomicBaseModel):
    first_name = None
    last_name = None
    username = None
    last_login = None
    date_joined = None

    # COMMENTED OUT — unused for CivicView (may be needed for future admin features)
    # Reason: CivicView is a public dashboard with minimal admin-only authentication
    # firstName = models.CharField(verbose_name=_('First Name'), max_length=100, db_column='firstName')
    # lastName = models.CharField(verbose_name=_('Last Name'), max_length=100, db_column='lastName')

    # General info - KEEP: Required for basic authentication
    email = models.EmailField(verbose_name=_('Email'), max_length=100, unique=True, db_column="email")
    password = models.CharField(verbose_name=_('Password'), max_length=128, db_column="password")
    
    # COMMENTED OUT — unused for CivicView (level-based permissions not needed)
    # Reason: CivicView uses simple is_staff/is_superuser for admin access only
    # level = models.IntegerField(verbose_name=_('Level'), null=False, blank=False, db_column="level", choices=USER_CHOICES)
    
    # COMMENTED OUT — unused for CivicView (no user profiles, phone verification, or profile pictures)
    # Reason: Public dashboard doesn't require user registration or profiles
    # phoneNumber = models.CharField(verbose_name=_('Phone Number'), max_length=20, db_column="phone_number")
    # profilePicture = models.URLField(verbose_name=_('Profile Picture'), max_length=512, db_column="profile_picture", null=True,)
    
    # User permissions - KEEP: Required for Django admin access
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True, db_column="is_active")
    is_staff = models.BooleanField(verbose_name=_('Is Staff'), default=False, db_column="is_staff")
    is_superuser = models.BooleanField(verbose_name=_('Is Superuser'), default=False, db_column="is_superuser")
    
    # COMMENTED OUT — unused for CivicView (no email verification workflow)
    # Reason: Admin accounts created manually, no public user registration
    # isVerified = models.BooleanField(verbose_name=_('Is Verified'), default=False, db_column="is_verified")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        # Updated for CivicView: Use email since firstName/lastName are commented out
        return self.email

    class Meta:
        db_table = "users"
        verbose_name_plural = "user"
        managed = True


# COMMENTED OUT — unused for CivicView
# Reason: No push notifications or multi-device support needed
# DEVICES_CHOICES = (
#     ("android", "android"),
#     ("ios", "ios"),
#     ("ipad", "ipad"),
#     ("web", "web"),
# )

# LANGUAGE_CHOICES = (
#     ('en', 'en'),
#     ('fr', 'fr'),
# )


# COMMENTED OUT — unused for CivicView
# Reason: No user devices tracking or push notifications needed
# class UsersDevices(AtomicBaseModel):
#     userId = models.ForeignKey(
#         Users,
#         verbose_name=_('User Id'),
#         related_name="users_devices",
#         db_column="user_id",
#         on_delete=models.CASCADE,
#     )
#     deviceId = models.CharField(
#         verbose_name=_('Device Id'),
#         max_length=500,
#         db_column="device_id",
#     )
#     token = models.CharField(
#         verbose_name=_('Token'),
#         max_length=500,
#         db_column="token",
#     )
#     deviceType = models.CharField(
#         verbose_name=_('Device Type'),
#         max_length=500,
#         db_column="device_type",
#         choices=DEVICES_CHOICES,
#     )
#     info = models.CharField(
#         verbose_name=_('Info'),
#         max_length=500,
#         db_column='device_info',
#         null=True
#     )
#     language = models.CharField(
#         verbose_name=_('Language'),
#         max_length=10,
#         db_column='language'
#     )
#
#     class Meta:
#         db_table = "users_devices"
#         verbose_name_plural = "users_device"
#         managed = True


# COMMENTED OUT — unused for CivicView
# Reason: No data export functionality needed for public dashboard
# class ExportData(AtomicBaseModel):
#     userId = models.ForeignKey(
#         Users,
#         verbose_name=_('User Id'),
#         related_name="export_data",
#         db_column="user_id",
#         on_delete=models.CASCADE,
#     )
#     modelName = models.CharField(
#         verbose_name=_('Model Name'),
#         max_length=500,
#         db_column="model_name"
#     )
#     fileUrl = models.URLField(
#         verbose_name=_('File Url'),
#         max_length=512,
#         db_column="file_url",
#     )
#
#     class Meta:
#         db_table = "export_data"
#         verbose_name_plural = "export_data"
#         managed = True
