import factory
from snippets.models import Snippet


class SnippetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Snippet
