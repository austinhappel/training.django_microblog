from django.contrib import messages
from django.views.generic import CreateView, ListView

from djangor.forms import EntryForm
from djangor.models import Entry
from django.db.models import Count
from taggit.models import Tag
from django.shortcuts import render_to_response


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

def count_tag(*args, **kwargs):
    tags = Entry.tags.through.objects.values('tag').distinct().annotate(Count('tag')).order_by('-tag__count')
    li= []
    for tag in tags:
        print tag
        name = Tag.objects.get(pk=int(tag['tag'])).name
        count = int(tag['tag__count'])
        li.append({'tagname' : name, 'count' : count})
    return render_to_response('djangor/count_tag.html', {'tagcloud': li})


