from django.contrib import admin

# Register your models here.

from .models import Post, Category, Comment, Tag, FavoriteBlog, CommentChild , CommentLike

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(FavoriteBlog)
admin.site.register(CommentChild)
admin.site.register(CommentLike)
