from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time,date,datetime

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=50,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.vendor_name

    def is_open(self):
        today_date= date.today()
        today = today_date.isoweekday()
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day = today)
        now=datetime.now()
        current_time  = now.strftime('%H:%M:%S')
        is_open = None
        for i in current_opening_hours:
            start = str(datetime.strptime(i.from_hours,'%I:%M %p' ).time())
            end = str(datetime.strptime(i.to_hours,'%I:%M %p' ).time())
            if current_time > start and current_time < end:
                is_open = True
            else:
                is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update vendor status
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_aproval_email.html"
                context={
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True:
                    # Send notification Email
                    mail_subject="Congratulations! Your restaurant has been approved"
                    # send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject="Sorry, You are not elgible to pblish your restaurant on our website"
                    # send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs) # Call the real save() method


DAYS=[
    (1,("Monday")),
    (2,("Tuesday")),
    (3,("Wednesday")),
    (4,("Thursday")),
    (5,("Friday")),
    (6,("Saturday")),
    (7,("Sunday")),
]

HOURS_OF_DAYS= [(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0,30)]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hours = models.CharField(choices=HOURS_OF_DAYS, max_length=10, blank=True)
    to_hours = models.CharField(default=False, choices=HOURS_OF_DAYS, max_length= 10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day','-from_hours')
        unique_together = ('vendor','day','from_hours','to_hours')

    def __str__(self) -> str:
        return self.get_day_display()
