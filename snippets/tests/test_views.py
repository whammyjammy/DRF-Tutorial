from django.urls import reverse
from rest_framework.test import APITestCase

from snippets.models import Snippet
from snippets.tests.factory import SnippetFactory


class SnippetListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('snippet_list')

    def test_get_returns_correct_number_of_items(self):
        # given
        snippet_count = 10
        SnippetFactory.create_batch(snippet_count)

        # when
        response = self.client.get(self.url)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), snippet_count)

    def test_post_creates_new_items(self):
        # given
        data = {
            'title': 'Title',
            'code': 'Code',
            'linenos': True,
        }

        # when
        response = self.client.post(self.url, data)

        # then
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Snippet.objects.filter(**data).exists())
        self.assertEqual(Snippet.objects.filter(**data).count(), 1)

    def test_post_returns_error(self):
        # given
        data = {
            'title': 'Title',
            'code': 'print()',
            'linenos': 'false',
            'language': 'fafafmfmqw'
        }
        # When
        response = self.client.post(self.url, data)

        # Then
        self.assertEqual(response.status_code, 400)


class SnippetsDetailViewTestCase(APITestCase):
    def test_snippet_does_not_exist_returns_error(self):
        # Given
        SnippetFactory.create_batch(10)
        url = reverse('snippet_detail', kwargs={'pk': 200})

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def test_get_returns_correct_value(self):
        # given
        data = {
            'title': 'Title',
            'code': 'Code',
            'linenos': True,
        }
        snippet = SnippetFactory.create(**data)

        url = reverse('snippet_detail', kwargs={'pk': snippet.pk})

        # when
        response = self.client.get(url)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['code'], data['code'])
        self.assertEqual(response.json()['linenos'], data['linenos'])

    def test_put_creates_new_item(self):
        # given
        data = {
            'title': 'New Title',
            'code': 'print',
            'linenos': True,
        }
        snippet = SnippetFactory.create()

        url = reverse('snippet_detail', kwargs={'pk': snippet.pk})

        # when
        response = self.client.put(url, data)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['code'], data['code'])
        self.assertEqual(response.json()['linenos'], data['linenos'])

    def test_put_updates_existing_item(self):
        # given
        data = {
            'title': 'New Title',
            'code': 'Print new',
            'linenos': True
        }
        snippet = SnippetFactory.create()
        url = reverse('snippet_detail', kwargs={'pk': snippet.pk})

        response = self.client.put(url, data)

        # when
        data['title'] = 'Changed Title'
        response = self.client.put(url, data)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], data['title'])

    def test_put_returns_error(self):
        # when
        data = {
            'title': 'Title',
            'code': 'Django',
            'linenos': "hehejajehe"
        }
        snippet = SnippetFactory.create()

        url = reverse('snippet_detail', kwargs={'pk': snippet.pk})

        # when
        response = self.client.put(url, data)

        # then
        self.assertEqual(response.status_code, 400)

    def test_delete_trunkates_snippet(self):
        # given
        data = {
            'code': 'print(hello World)'
        }
        snippet = SnippetFactory.create(**data)

        url = reverse('snippet_detail', kwargs={'pk': snippet.pk})

        # when
        response = self.client.delete(url)

        # then
        self.assertEqual(response.status_code, 204)
