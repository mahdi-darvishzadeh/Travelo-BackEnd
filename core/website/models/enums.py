from django.db import models

# define your enums here

class NotificationEnum(models.TextChoices):
    CONFIRM_YOUR_EMAIL = 1
    EMAIL_IS_VERIFIED = 2
    YOUR_EMAIL_HAS_BEEN_CHECKED = 3
    CHECK_IN_MUST_BE_DONE = 4