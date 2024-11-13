from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions #импортируем декоратор для перевода и класс настроек,
# от которого будем наследоваться

#регистрируем наши модели для перевода

# @register(Category)
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('category', ) #указываем, какое именно поле нужно переводить в виде кортежа
#
# @register(Post)
# class PostTranslationOptions(TranslationOptions):
#     fields = ('text','title' )