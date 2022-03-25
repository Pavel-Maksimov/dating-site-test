from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


GENDER_CHOICES = (
    ('мужской', 'мужской'),
    ('женский', 'женский'),
)


class ClientManager(BaseUserManager):
    """Define a model manager for Client model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a Client with the given email and password."""

        if not email:
            raise ValueError('Это поле является обязательным.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular Client with the given
        email and password.
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Поле is_superuser для суперпользователя должно'
                'быть установлено True.'
            )

        return self._create_user(email, password, **extra_fields)


class Client(AbstractUser):
    """Define a Client model."""

    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'имя',
        max_length=150
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150
    )
    gender = models.CharField(
        'пол',
        max_length=50,
        choices=GENDER_CHOICES
    )
    avatar = models.ImageField(
        'аватарка',
        upload_to='avatars/'
    )
    password = models.CharField(
        'пароль',
        max_length=150
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'gender',)

    objects = ClientManager()


class Like(models.Model):
    matcher = models.ForeignKey(
        Client, on_delete=models.CASCADE,
        related_name='likes_from'
    )
    matched = models.ForeignKey(
        Client, on_delete=models.CASCADE,
        related_name='likes_to'
    )
    like = models.BooleanField()

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        models.UniqueConstraint(
            fields=('matcher', 'matched'),
            name='unique_like'
        )

        def __str__(self):
            return f'Оценка {self.matcher} пользователя {self.matched}'
