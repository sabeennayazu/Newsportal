from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from newspaper.forms import ContactForm, NewsletterForm
from newspaper.models import Category, Post, Tag,Contact, NewsLetter
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from datetime import timedelta
from newspaper.models import Advertisement
from newspaper.forms import CommentForm
from django.http import JsonResponse

# Create your views here.
class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.filter(
            published_at__isnull=False, status='active'
        ).order_by('-published_at')[:5]
        context['advertisement'] = (
            Advertisement.objects.all().order_by('-created_at').first()  # Assuming you have an Advertisement model
        )
        return context


class HomeView( SidebarMixin, ListView):
    model = Post
    template_name = 'newsportal/home.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(
        published_at__isnull=False,status='active'
    ).order_by('-published_at')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_post'] = (
            Post.objects.filter(
                published_at__isnull=False, status='active'
            ).order_by('-published_at', "-views_count").first()
        )
        
        
        one_week_ago = timezone.now() - timedelta(days=7)
        context['weekly_top_posts'] = Post.objects.filter(
            published_at__isnull=False, status='active',
            published_at__gte = one_week_ago
        ).order_by('-published_at','-views_count')[:5]

      


        return context

class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = 'newsportal/list/list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status='active'
        ).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        return context

class PostDetailView(SidebarMixin, DetailView):
    model = Post
    template_name = 'newsportal/detail/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status='active')
        return query
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        
        context['related_posts'] = Post.objects.filter(
            published_at__isnull=False, status='active',category=self.object.category
        ).order_by('-published_at','-views_count')[:2]
    
    

        return context

class Commentview(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST['post']
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('post-detail', post_id)
        else:
            post = Post.objects.get(pk=post_id)
            popular_posts = Post.objects.filter(
                published_at__isnull=False, status='active'
            ).order_by('-published_at')[:5]
            Advertisement = (
                Advertisement.objects.all().order_by('-created_at').first()
            )
            return render(request, 'newsportal/detail/detail.html',
             {
                'post': post,
                'form': form,
                'popular_posts': popular_posts,
                'advertisement': Advertisement,
                
                },
                )

class PostByCategoryView(SidebarMixin, ListView):
    model = Post
    template_name = 'newsportal/list/list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False, status='active',
            category__id=self.kwargs['category_id'],
        ).order_by('-published_at')
        return query

class CategoryListView(ListView):
    model = Category
    template_name = 'newsportal/categories.html'
    context_object_name = 'categories'

class PostByTagView(SidebarMixin, ListView):
    model = Post
    template_name = 'newsportal/list/list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False, status='active',
            tags__id=self.kwargs['tags_id'],
        ).order_by('-published_at')
        return query

class TagListView(ListView):
    model = Tag
    template_name = 'newsportal/tags.html'
    context_object_name = 'tags'

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = 'newsportal/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

class NewsletterView(View):

    def post(self, request):
        is_ajax = request.headers.get('x-requested-with')
        if is_ajax == 'XMLHttpRequest':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing to our newsletter!'}, status=201)
            else:
                return JsonResponse({'success': False, 'message': 'cannot subscribe'},status=400)
        else:
             return JsonResponse({'success': False, 'message': 'Cannot process. Must be an AJAX request'}, status=400)