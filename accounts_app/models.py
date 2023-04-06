from django.db import models
from django.contrib.auth.models import User
# Create your models here.





STATE_CHOICES = (
    
   ('Assam', 'Assam'),
   ('Delhi', 'Delhi'),
   ('Kerala', 'Kerala'),
   ('Punjab', 'Punjab'),
   ('Haryana', 'Haryana'),
   ('Rajasthan', 'Rajasthan'),
   ('Karnataka', 'Karnataka'),
   ('Madhya Pradesh', 'Madhya Pradesh'),
   ('Uttar Pradesh', 'Uttar Pradesh'),
   ('Jammu & Kashmir', 'Jammu & Kashmir'),
  
    
)

# user profile model here extend
class Profile(models.Model):
    """User Profile Model for adding information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio  = models.TextField(default='Write details/description about your self. Like you can also describe your past experiences as well',   max_length=500)
    pic  = models.ImageField(upload_to='Profile/images', blank=True)
    address = models.CharField(max_length=78, default='Jalandhar, Punjab')


class Address(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   name  = models.CharField(max_length=200)
   city  = models.CharField(max_length=200)
   state  = models.CharField(choices=STATE_CHOICES,  max_length=200)
   pincode = models.IntegerField()

   def __str__(self):
      return str(self.name) + '|' +  str(self.state)
