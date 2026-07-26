"""
Class-Based Views (CBVs) for the Podcasts application.
Handles rendering podcast feeds, detailed episode views, and comment processing.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import Podcast
from .forms import PodcastForm, PodcastCommentForm

class PodcastCreateView(CreateView):
    """
    View for rendering and processing the podcast creation form.
    """
    model = Podcast
    form_class = PodcastForm
    template_name = 'podcasts/podcast_form.html'
    success_url = reverse_lazy('podcasts:list')


class PodcastListView(ListView):
    """
    View for displaying a paginated list of published podcasts.
    Includes basic search functionality based on the episode title.
    """
    model = Podcast
    template_name = 'podcasts/podcast_list.html'
    context_object_name = 'podcasts' 
    paginate_by = 9 

    def get_queryset(self):
        """
        Retrieves active podcasts, optimized with select_related for the host.
        """
        # OPTIMIZATION: Prevent N+1 query when displaying the host's name
        qs = Podcast.objects.select_related('host').filter(is_published=True).order_by('-created_at')
        query = self.request.GET.get('q')
        
        # Handle search input from the user
        if query:
            qs = qs.filter(title__icontains=query) 
        return qs


class PodcastDetailView(DetailView):
    """
    View for displaying a single podcast episode along with its comments.
    Handles both GET requests (viewing) and POST requests (submitting comments).
    """
    model = Podcast
    template_name = 'podcasts/podcast_detail.html'
    context_object_name = 'podcast' 

    def get_queryset(self):
        """
        Restricts access to only published podcasts.
        """
        return Podcast.objects.select_related('host').filter(is_published=True)
  
    def get_context_data(self, **kwargs):
        """
        Injects the comment form, active comments, related podcasts, and pagination nodes into the context.
        """
        context = super().get_context_data(**kwargs)
        
        # Instantiate an empty form for new comments
        context['form'] = PodcastCommentForm()
        
        # Fetch only active comments utilizing the related_name defined in the model
        context['comments'] = self.object.comments.filter(active=True)
        
        # Fetch related podcasts excluding the current one
        context['related_podcasts'] = Podcast.objects.select_related('host').exclude(id=self.object.id).order_by('-created_at')[:6]
        
        # Handle Next/Previous episode navigation safely
        try:
            context['next_podcast'] = self.object.get_next_by_created_at(is_published=True)
        except Podcast.DoesNotExist:
            context['next_podcast'] = None
            
        try:
            context['previous_podcast'] = self.object.get_previous_by_created_at(is_published=True)
        except Podcast.DoesNotExist:
            context['previous_podcast'] = None
            
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the submission of a new comment.
        Implements the PRG (Post/Redirect/Get) pattern to prevent duplicate submissions on page reload.
        """
        self.object = self.get_object() 
        
        # Copy POST data to manipulate it safely without altering the immutable request.POST dict
        data = request.POST.copy()
        
        # Handle 'unknown' username and sanitize inputs
        if not data.get('username') or data.get('username').strip() == '':
            data['username'] = 'غير معروف'
        else:
            data['username'] = data['username'].strip()
            
        if data.get('comment'):
            data['comment'] = data.get('comment').strip()
            
        form = PodcastCommentForm(data)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.podcast = self.object
            
            # Additional safety strip (redundant but safe)
            if comment.comment:
                comment.comment = comment.comment.strip()
            if comment.username:
                comment.username = comment.username.strip()
                
            comment.save() 
            
            # Redirect back to the same page with an anchor to the comments section
            return redirect(reverse('podcasts:detail', kwargs={'slug': self.object.slug}) + '#comments-section')
        
        # If the form is invalid, re-render the page with form errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
        
        # TODO: Consider separating the POST handling into a dedicated FormView or utilizing Django's FormMixin.