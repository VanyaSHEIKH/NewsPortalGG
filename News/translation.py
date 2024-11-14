from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions
# от которого будем наследоваться


# @register(Category)
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('category', ) #указываем, какое именно поле нужно переводить в виде кортежа
#
# @register(Post)
# class PostTranslationOptions(TranslationOptions):
#     fields = ('text','title' )
