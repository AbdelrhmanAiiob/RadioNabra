from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Podcast, PodcastComment
from .forms import PodcastForm, PodcastCommentForm

# ChildCreateView
class PodcastCreateView(CreateView):
  model = Podcast
  form_class = PodcastForm
  template_name = 'podcasts/podcast_form.html'
  success_url = reverse_lazy('podcasts:list')


# ChildFeildView
class PodcastListView(ListView):
  model = Podcast
  template_name = 'podcasts/podcast_list.html'
  context_object_name = 'podcasts' 

  paginate_by = 9 

  def get_queryset(self):
    qs= Podcast.objects.select_related('host').filter(is_published=True).order_by('-created_at')
    query= self.request.GET.get('q')
    
    # if userSearch
    if query:
      qs= qs.filter(title__icontains=query) 
    return qs


# ChildFeildDetailView
class PodcastDetailView(DetailView):
  model = Podcast
  template_name = 'podcasts/podcast_detail.html'
  context_object_name = 'podcast' 

  def get_queryset(self):
    return Podcast.objects.select_related('host').filter(is_published=True)
  
  # CommentsSide(GET-CommentRead-)
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = PodcastCommentForm()
    # Fetching comments specific to this podcast
    context['comments'] = self.object.comments.filter(active=True)
    context['related_podcasts'] = Podcast.objects.select_related('host').exclude(id=self.object.id).order_by('-created_at')[:6]
    
    # pagination pages control for next and previous podcasts
    try:
      context['next_podcast'] = self.object.get_next_by_created_at(is_published=True)
    except Podcast.DoesNotExist:
      context['next_podcast'] = None
    try:
      context['previous_podcast'] = self.object.get_previous_by_created_at(is_published=True)
    except Podcast.DoesNotExist:
      context['previous_podcast'] = None
    return context

# CommentsSide(POST-AddComment-)
def post(self, request, *args, **kwargs):
  self.object = self.get_object() 
  
  # PRG Pattern: Using copy to manipulate POST data safely
  data = request.POST.copy()
  
  # Handle 'unknown' username and strip whitespaces
  if not data.get('username') or data.get('username').strip() == '':
    data['username'] = 'غير معروف'
  else:
    data['username'] = data['username'].strip()
  # Strip whitespaces from comment
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
  
  # If the form is invalid, re-render the page with errors
  context = self.get_context_data(**kwargs)
  context['form'] = form
  return self.render_to_response(context)