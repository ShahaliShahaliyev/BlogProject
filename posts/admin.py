from django.contrib import admin

from .models import Author, Category, IpModel, Post,Info

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Info)
admin.site.register(IpModel)