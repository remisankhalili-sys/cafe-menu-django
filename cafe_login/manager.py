from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user_object(self, phone, email, password=None):
        if not phone:
            raise ValueError("شماره تلفن نامعتبر است!")
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            user.save(using=self._db)
        return user
    def create_user(self, phone, email, password=None):

        user = self.create_user_object(phone, email, password=None)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, email=None, password=None):
        user = self.create_user_object(phone, email, password=None)
        user.is_superuser = True
        user.is_staff = True
        user.admin = True
        user.save(using=self._db)

        return user

   