from django.contrib import messages
from django.views.generic import CreateView

from djangor.forms import EntryForm
from djangor.models import Entry

from django.shortcuts import render_to_response
import re

class AddEntryView(CreateView):
    """Generic view for creating a new entry

    Django generic views are instantiated with a reference to the current 
    request (self.request).  We can use this to get hold of the currently 
    authenticated user and use that to tie the new entry to a User object
    """
    def form_valid(self, form):
        # saving the form while passing commit=False will ensure that no
        # attempt is made to save the object created by the form.  This allows
        # us to manually set values we need, like the author.  See the model
        # save method to find out how we get pub_date automatically.
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        # we can use the django messages framework to pass information back
        # to the user.  Here we alert the user that their entry was saved.
        msg = "Your post, %s, has been published"
        messages.add_message(self.request, messages.INFO, msg % self.object)
        return super(AddEntryView, self).form_valid(form)

def tag_search(request, *args, **kwargs):
    for i in args:
        tag = i
    entries = Entry.objects.filter(tags__name__in=[tag])
    return render_to_response('djangor/entry_list.html', {'tag': tag, 'entries': entries })
    
