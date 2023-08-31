from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save, sender = User)
def post_save_create_profile_receiver(sender, instance,created, **kwargs):
    print(created)
    if created:
        profile=UserProfile.objects.create(user = instance)
        profile.save()
        # print("created the user profile")
    else:
        try:
            profile= UserProfile.objects.get(user = instance)
            profile.save()
        except:
            # Create the UserProfile id not exist
            UserProfile.objects.create(user=instance)
            # print("Profile was not exists  but i creates one")

        print("User is now created")
# post_save.connect(post_save_create_profile_receiver,sender=User)  # this is one method of creating a signal


def pre_save_create_profile_receiver(sender,instance,**kwargs):
    # print(instance.username, "This user is being save")
    pass

pre_save.connect(pre_save_create_profile_receiver,sender=User)