from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
import random
import string
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUser(AbstractUser):
    is_verified_email = models.BooleanField(default=False)

class EmailVerification(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    @classmethod
    def create_verification(cls, user):
        code = ''.join(random.choices(string.digits, k=6))
        return cls.objects.create(code=code, user=user)

    def send_verification_email(self):
        send_mail(
            'Subject here',
            f'Verification code: {self.code}',
            'takhmina716@gmail.com', 
            [self.user.email],
            fail_silently=False,
        )

class Tour(models.Model):
    city = models.CharField(max_length=255)
    time = models.TimeField()
    day = models.CharField(max_length=255)
    date = models.DateField()

class TourRequest(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def clean(self):
        if self.user.tourrequest_set.filter(tour=self.tour, is_approved=True).exists():
            raise ValidationError("Вы уже отправили заявку на этот тур и она была одобрена.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
