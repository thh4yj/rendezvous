from django.db import models
from django import forms
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from .validators import validate_file_extension
import re
import datetime
import pytz

# Create your models here.

class Event(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    desc = models.TextField(max_length = 5000)
    location_name = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200, blank = True)
    pub_date = models.DateTimeField('Date Published')
    start = models.DateTimeField('Start date')
    end = models.DateTimeField('End date')
    icon = models.ImageField(upload_to = 'images', blank = True, validators = [validate_file_extension])
    rsvps = models.IntegerField(default=0)
    people_going = ArrayField(base_field = models.CharField(max_length = 200, blank = True), default = list)
    # Additional images for carousel - array of ImageFields?

    def __str__(self):
        return self.title

    # These methods ensure that data is correct and accurate based on logic
    def valid_address(self, address):
        x = re.search(r'\b\d{1,3}(?:\s[a-zA-Z\u00C0-\u017F]+)+', address)
        return x

    def valid_time(self, tm):
        if (tm != None):
            now = timezone.now()
            return now <= tm
        else:
            return False
    
    def valid_date_format(self, tm):
        if tm:
            try:
                date = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M')
            except ValueError:
                return False

            return True
        else:
            return False

    def valid_interval(self, tm1, tm2):
        valid1 = self.valid_time(tm1)
        valid2 = self.valid_time(tm2)

        if (valid1 and valid2 and not (tm1 == None) and not (tm2 == None)):
            return tm1 < tm2
        else:
            return False

    def exists_required_input(self, name, desc, location, address, start, end):
        if (len(name) > 0 and len(location) > 0 and len(desc) > 0 and self.valid_interval(start, end)):
            return 0
        else:
            if (len(name) == 0):
                return 1
            elif (len(location) == 0):
                return 2
            elif (len(desc) == 0):
                return 3
            elif not self.valid_interval(start, end):
                return 4
            elif not (self.valid_address(address) or address.strip() == ""):
                return 5
            else:
                return 6

# Source: https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
# EventForm follows a similar structure as the example ModelForm
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'desc', 'location_name', 'address', 'start', 'end', 'icon']
        widgets = {
            'desc': forms.Textarea(attrs = {'rows': 10, 'cols': 120}),
            'start': forms.DateTimeInput(attrs = {'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs = {'type': 'datetime-local'})
        }

