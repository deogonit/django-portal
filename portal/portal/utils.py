from django.utils.text import slugify
from django.db.models import Model
from time import time


def unique_slug_generator(models_instance: Model, title, slug_field):
    slug = slugify(title, allow_unicode=True)
    model_class = models_instance.__class__

    if model_class.default_manager.filter(slug=slug).exists():
        slug = '{}-{}'.format(slug, str(int(time())))

    return slug
