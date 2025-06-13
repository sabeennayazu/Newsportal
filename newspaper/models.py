from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #dont create a table for this model in db

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    icons = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        """Return the string representation of the tag."""
        return self.name
    
class Post(TimeStampedModel):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('in_active', 'Inactive'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='post_images/%Y/%m/%d', blank=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you have User model from auth
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
       
        return self.title
    
class Advertisement(TimeStampedModel):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='advertisements/%Y/%m/%d', blank=False)
   

    def __str__(self):
        return self.title

class UserProfile(TimeStampedModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/%Y/%m/%d', blank=False)
    address = models.CharField(max_length=205)
    biography = models.TextField()

    def __str__(self):
        return self.user.username

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.content[:50]} | {self.user.username}'

class Contact(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['created_at']

class NewsLetter(TimeStampedModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
   

    

    
    