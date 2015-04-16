from django import test

from cms.models import Navigation, Article


class CmsTests(test.TestCase):

    def setUp(self):
        article = Article.objects.create(slug="test", text="We are here!")
        Navigation.objects.create(article=article, text="test", order=1)

    def test_second_request_should_not_touch_database(self):
        response = self.client.get("/")
        self.assertTrue("We are here!" in response.content)
        with self.assertNumQueries(0):
            response = self.client.get("/")
            self.assertTrue("We are here!" in response.content)
