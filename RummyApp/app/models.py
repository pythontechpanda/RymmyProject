from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import string
import random

class State(models.Model):
    name  = models.CharField(max_length=300, null=True)

def filepath_profile(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('profile/', filename)

def generate_random_string():
    """Generate a random string of letters and digits."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class User(AbstractUser):
    profile_picture=models.FileField(upload_to=filepath_profile, default='profile/user.png')
    mobile_no = models.CharField(max_length=12, unique=True)
    middle_name = models.CharField(max_length=200, null=True)
    date_of_birth = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=300, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    pincode = models.CharField(max_length=300, null=True)
    is_verified=models.BooleanField(default=False)
    device_registration_id=models.CharField(max_length=500,null=True)
    is_above18=models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    refer_code=models.CharField(max_length=50,default=0)
    
    # random username or password
    
    
    
    # random username or password
    def save(self, *args, **kwargs):
        # Generate username based on mobile number and a random string
        if not self.username:
            random_string = generate_random_string()
            self.username = f"{self.mobile_no[:4]}{random_string}"

        # Set the password the same as the username
        if not self.password:
            self.set_password(self.username)

        super().save(*args, **kwargs)
    