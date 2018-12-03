from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from django.shortcuts import render
from datetime import datetime

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(Page):
    body = RichTextField(blank=True)
    date = models.DateTimeField()
    spots_available = models.PositiveIntegerField(default=0)
    waitlist_spots_available = models.PositiveIntegerField(default=0)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('date', classname="full"),
        FieldPanel('spots_available', classname="full"),
        FieldPanel('waitlist_spots_available', classname="full"),
    ]

    #We need some type of validation that disallows the event administrator to reduce the spots available or the waitlist below the
    #current number of registered spots or waitlisted spots

    #https://docs.djangoproject.com/en/2.1/intro/tutorial07/
    #https://stackoverflow.com/questions/24802244/custom-validation-in-django-admin
    #https://docs.djangoproject.com/en/2.1/ref/forms/validation/

    def serve(self, request):
            from ppl_registration.forms import UserForm
            event_instance = Event.objects.get(id=self.page_ptr_id)
            current_registered = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=0).count()
            current_waitlisted = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=1).count()
            current_spots = self.spots_available - current_registered
            current_waitlist_spots = self.waitlist_spots_available - current_waitlisted

            if request.method == 'POST':
                user_form = UserForm(request.POST)
                if user_form.is_valid() and current_spots > 0:
                    user = user_form.save()
                    user_instance = user
                    #insert the values into the registration table
                    registration = Registration(user_name=user_instance, event_name=event_instance, wait_list=0)
                    registration.save()
                    #There is a bug here. When the admin changes the spots available or the waitlist amount after people start registering
                    #The spots available won't be reflected. This is also true for the waitlist. Also deleting a registration in the admin doesn't re-add a spot in spots available
                        #update_spot = event_instance
                        #update_spot.spots_availabPrintingle = self.initial_spots - 1
                        #update_spot.save(update_fields=['spots_available'])
                        #next issue: Validation based on the user's first and last names

                    return render(request, 'ppl_registration/thank_you.html', {
                        'page': self,
                        'user': user,
                    })

                elif user_form.is_valid() and current_spots ==0 and current_waitlist_spots > 0:
                    user = user_form.save()
                    user_instance = user
                    registration = Registration(user_name=user_instance, event_name=event_instance, wait_list=1)
                    registration.save()

                    return render (request, 'ppl_registration/waitlist.html', {
                    'page':self,
                    'user':self,
                    })

                else:
                    return render(request, 'ppl_registration/full.html', {
                        'page': self,
                    })
            else:
                user_form = UserForm()

            return render(request, 'ppl_registration/event.html', {
                'page': self,
                'current_registered': current_registered,
                'current_waitlisted': current_waitlisted,
                'current_spots': current_spots,
                'current_waitlist_spots': current_waitlist_spots,
                'user_form': user_form,
                'event_instance': event_instance,
    })


class Registration(models.Model):
    user_name = models.ForeignKey('User', default=1, on_delete=models.CASCADE)
    event_name = models.ForeignKey('Event', default=1, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True, blank=True)
    wait_list = models.BooleanField(default=0)
    def __str__(self):
        return self.event_name.title + ' ' + self.user_name.first_name + ' ' + self.user_name.last_name

#We need a way to delete all users associated with the event when we delete the event
#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/add_actions.html
