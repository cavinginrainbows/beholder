from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User

# Create your models here.

class Issue(models.Model):
    issue_num = models.IntegerField(unique=True)
    release_date = models.DateField()
    cover_img_url = models.URLField(null=True, blank=True)
    toc_img = models.ForeignKey('Content', on_delete=models.DO_NOTHING, null=True, related_name='in_issue')

    class Meta:
        db_table = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['-issue_num']

    def __str__(self):
        return f'issue {self.issue_num}'

    def get_absolute_url(self):
        return reverse('issuetoc', kwargs={"issue_num": self.issue.issue_num})

class Person(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    appears_in = models.ManyToManyField(Issue, related_name='contributors')
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'person'
        verbose_name_plural = 'people'
        ordering = ['first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Bio(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    pronouns = models.CharField(max_length=50, blank=True)
    pseudonym = models.CharField(max_length=50, blank=True)
    social_url = models.URLField(blank=True)
    person_url = models.URLField(blank=True)
    bio_text = models.TextField()
    bio_img_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'bio'
        verbose_name_plural = 'bios'
        ordering = ['person']

    def __str__(self):
        return f'{self.person}\'s bio'


class Content(models.Model):
    #Content type choices, for choosing css class:
    POEM = 'poem'
    LONG_FORM = 'long'
    SHORT_FORM = 'short'
    COMIC = 'comic'
    GALLERY = 'gallery'
    SOLO_IMG = 'soloimg'
    ED_NOTE = 'ednote'

    CONTENT_CHOICES = [
        (POEM, 'poem'),
        (LONG_FORM, 'long form'),
        (SHORT_FORM, 'short form'),
        (COMIC, 'comic'),
        (GALLERY, 'image gallery'),
        (SOLO_IMG, 'single image'),
        (ED_NOTE, 'editors note'),
    ]

    title = models.CharField(max_length=250, blank=True, default="")
    creator = models.ManyToManyField(Person, related_name='contributions')
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='contents')
    slug = models.SlugField(max_length=200, unique=True)
    pub_date = models.DateField()
    metades = models.CharField(max_length=300, default="magazine page")
    page = models.IntegerField()
    css_class = models.CharField(max_length=7, choices=CONTENT_CHOICES, default=SHORT_FORM)
    body = models.TextField(blank=True)
    img_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'content'
        verbose_name_plural = 'contents'
        ordering = ['page']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('contentdetail', kwargs={"issue_num": self.issue.issue_num, "slug": self.slug})

    def get_content_class(self):
        return self.css_class

    def next(self):
        end = self.issue.contents.last()
        if self == end:
            return None
        else: 
            nxt = self.page + 1
            return self.issue.contents.get(page=nxt)

    def previous(self):
        if self.page == 1:
            return None
        else:
            prv = self.page - 1
            return self.issue.contents.get(page=prv)
