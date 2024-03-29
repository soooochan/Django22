from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

#### Tag 모델 만들기 ####
class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length =200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True) # 동일한 name을 갖는 카테고리를 만들 수 있다 .
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True) # 사람이 읽을 수 있는 텍스트로 고유 URL
    # slug는 name에 대한 url 값이다

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # Meta로 모델의 복수형 알려주기
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # 추후 author 작성 user table에 등록되어 있는 것을 가져옴 ( 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때
    # 작성자명을 빈 칸으로 둔다'
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # delete를 쓰게 되면 author 카테고리가 삭제가 된다. null=True : author이 삭제되면 null로 바뀐다.

    # Post 모델에 category 필드 추가하기 ( 관리자 페이지에서 카테고리를 빈 칸으로 지정할 수 있게 된다. )
    category=models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) # 카테고리를 빈칸으로 두기 (blank = True)
    tags = models.ManyToManyField(Tag, blank=True)



    # ' 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트도 같이 삭제한다.'
    # author = models.ForeignKey(User, on_delete=models.CASCADE)





    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # a.b.text => a b text

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #사용자가 지워지면 댓글도 지워지게끔
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'


