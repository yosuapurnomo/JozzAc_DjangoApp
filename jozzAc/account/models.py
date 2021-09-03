from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.
class AccountManage(BaseUserManager):
	use_in_migrations = True


	def _create_user(self, username, password, **extra_fields):
		if not username:
			raise ValueError('The given email must be set')
		username = username
		user = self.model(username=username, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_admin', True)
		return self._create_user(username, password, **extra_fields)

	def create_superuser(self, username, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('jabatan', "ADMIN")
		# print(extra_fields)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
	jabatanChoice        = [
	('ADMIN','ADMIN'),
	('TEKNISI','TEKNISI'),
	]
	username 	= models.CharField(max_length=20, unique=True) 
	jabatan 	= models.CharField(choices=jabatanChoice, max_length=8)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login 	= models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	is_admin	= models.BooleanField(default=True)

	objects = AccountManage()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = 'Account'
		verbose_name_plural = 'Account'

# class Account(models.Model):
# 	jabatanChoice        = [
#         ('ADMIN','ADMIN'),
#         ('TEKNISI','TEKNISI'),
#     ]
# 	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
# 	jabatan			= models.CharField(choices=jabatanChoice, max_length=8)