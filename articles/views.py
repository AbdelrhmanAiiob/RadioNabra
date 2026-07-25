from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import  CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# ChildCreateView
class ArticleCreateView(CreateView):
  model= Article
  form_class= ArticleForm
  template_name= 'articles/article_form.html'
  success_url= reverse_lazy('articles:list')

# ChildFeildView
class ArticleListView(ListView):
  model = Article
  template_name= 'articles/article_list.html'
  context_object_name= 'articles' # in HTML variableName no='object' yes='article'

  paginate_by= 9 # how many article in singlePage

  def get_queryset(self):
    # إضافة select_related('author') هنا لمنع N+1 
    qs= Article.objects.select_related('author').filter(is_published=True).order_by('-created_at')
    query = self.request.GET.get('q')
    # if userSearch
    if query:
      qs = qs.filter(title__icontains=query) # specific search word
    return qs

# ChildFeildDetailView
class ArticleDetailView(DetailView):
  model = Article
  template_name= 'articles/article_detail.html'
  context_object_name= 'article' # in HTML variableName no='object' yes='article'

  def get_queryset(self):
    return Article.objects.select_related('author').filter(is_published=True)
  
  # CommentsSide(GET-CommentRead-)
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = CommentForm()
    context['comments'] = self.object.comment_set.all()
    context['related_articles'] = Article.objects.select_related('author').exclude(id=self.object.id).order_by('-created_at')[:6]
    
    # pagination pages control
    try:
      context['next_article']= self.object.get_next_by_created_at(is_published=True)
    except Article.DoesNotExist:
      context['next_article']= None
    try:
      context['previous_article']= self.object.get_previous_by_created_at(is_published=True)
    except Article.DoesNotExist:
      context['previous_article']= None
    return context
  
  # CommentsSide(POST-AddComment-)
  def post(self, request, *args, **kwargs):
    self.object = self.get_object() 
    
    data = request.POST.copy()
    
    if not data.get('username') or data.get('username').strip() == '':
      data['username'] = 'غير معروف'
    else:
      data['username'] = data['username'].strip()
    if data.get('comment'):
      data['comment'] = data.get('comment').strip()
    form = CommentForm(data)
    
    if form.is_valid():
      comment = form.save(commit=False)
      comment.article = self.object
      # strip spaces in comments
      if comment.comment:
        comment.comment = comment.comment.strip()
      if comment.username:
        comment.username = comment.username.strip()
      comment.save() 
      return redirect(reverse('articles:detail', kwargs={'slug': self.object.slug}) + '#comments-section')
    
    context = self.get_context_data(**kwargs)
    context['form'] = form
    return self.render_to_response(context)