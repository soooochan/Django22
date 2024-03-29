from django.contrib import admin
from .models import Post, Category, Tag, Comment
import os

# Register your models here.

admin.site.register(Post)
#admin.site.register(Category)



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)} # 카테고리 모델의 name 필드에 값이 입력될 때
    # 자동으로 slug가 만들어진다.


admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag, TagAdmin)


admin.site.register(Comment)