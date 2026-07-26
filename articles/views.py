"""
Class-Based Views (CBVs) for handling the business logic of the Articles application.
Includes listing, detailing, creating articles, and handling user comments.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

class ArticleCreateView(CreateView):
    """
    View for rendering and processing the article creation form.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:list')


class ArticleListView(ListView):
    """
    View for displaying a paginated list of published articles.
    Includes search functionality.
    """
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles' 
    paginate_by = 9 # Number of articles per page

    def get_queryset(self):
        """
        Retrieves articles optimized with select_related to prevent N+1 query issues.
        Filters by publication status and handles user search queries.
        """
        # OPTIMIZATION: select_related fetches the User (author) in the same query.
        qs = Article.objects.select_related('author').filter(is_published=True).order_by('-created_at')
        
        # Handle search input from the GET request
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query) 
            
        return qs


class ArticleDetailView(DetailView):
    """
    View for displaying a single article along with its comments.
    Also handles POST requests to submit new comments on the same page.
    """
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article' 

    def get_queryset(self):
        """
        Restricts access to only published articles.
        """
        return Article.objects.select_related('author').filter(is_published=True)
  
    def get_context_data(self, **kwargs):
        """
        Injects additional data (comment form, existing comments, related articles, 
        and pagination) into the template context.
        """
        context = super().get_context_data(**kwargs)
        
        # Inject an empty comment form
        context['form'] = CommentForm()
        
        # Fetch related comments
        context['comments'] = self.object.comment_set.all()
        
        # Fetch up to 6 recent articles excluding the current one
        context['related_articles'] = Article.objects.select_related('author').exclude(id=self.object.id).order_by('-created_at')[:6]
        
        # Handle Next/Previous article navigation safely
        try:
            context['next_article'] = self.object.get_next_by_created_at(is_published=True)
        except Article.DoesNotExist:
            context['next_article'] = None
            
        try:
            context['previous_article'] = self.object.get_previous_by_created_at(is_published=True)
        except Article.DoesNotExist:
            context['previous_article'] = None
            
        return context
  
    def post(self, request, *args, **kwargs):
        """
        Handles the submission of a new comment.
        Extracts, sanitizes, and saves the data securely.
        """
        self.object = self.get_object() 
        data = request.POST.copy()
        
        # Sanitize and handle anonymous users
        if not data.get('username') or data.get('username').strip() == '':
            data['username'] = 'غير معروف'
        else:
            data['username'] = data['username'].strip()
            
        if data.get('comment'):
            data['comment'] = data.get('comment').strip()
            
        form = CommentForm(data)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object # Link the comment to the current article
            
            # Final sanitization before saving
            if comment.comment:
                comment.comment = comment.comment.strip()
            if comment.username:
                comment.username = comment.username.strip()
                
            comment.save() 
            
            # Redirect to the same article page, anchored to the comments section
            return redirect(reverse('articles:detail', kwargs={'slug': self.object.slug}) + '#comments-section')
        
        # If the form is invalid, re-render the page with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
        
        # TODO: Refactor POST handling. Using Django's FormMixin with DetailView 
        # is a more robust pattern for handling forms alongside object details.