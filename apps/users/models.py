from django.db import models

from utils.base_model import BaseModel

# Create your models here.


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(max_length=40, unique=True)
    phone_regex = RegexValidator(
        regex=r'^(?:\+234|0)[789][01]\d{8}$',
        message="Phone number must be a valid Nigerian number (e.g., 08012345678 or +2348012345678)."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True
    )
    rider_number = models.CharField(max_length=40, unique=True, null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, editable=False, null=True)
    is_referral_qualified = models.BooleanField(default=False)
    referral_used = models.BooleanField(default=False)
    referral_used_purchase = models.BooleanField(default=False)
    
    # Telegram notification fields
    telegram_user_id = models.BigIntegerField(null=True, blank=True, unique=True, db_index=True)
    telegram_user_chat_id = models.CharField(max_length=100, null=True, blank=True)
    telegram_notifications_enabled = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        
        if not self.referral_code:
            self.referral_code = generate_referral_code(10).upper()
            
        super().save(*args, **kwargs)
        
    @property
    def check_referral_qualification(self):
        from utils.feature_flags import is_feature_enabled

        flag, enable = is_feature_enabled(FeatureNames.REFERRAL_SYSTEM.value)
        if not enable:
            return False

        successful_referrals = self.referrals_made.filter(successful=True).count()
        qualified = successful_referrals >= 5

        if self.is_referral_qualified != qualified:
            self.is_referral_qualified = qualified
            self.save(update_fields=["is_referral_qualified"])

        return qualified
    

    objects=UserManager( )
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['first_name',"last_name"]

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]
    
    def __str__(self):
        return f"{self.email}"
