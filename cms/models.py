from django.db import models


class Article(models.Model):
    slug = models.SlugField()
    text = models.TextField()

    def get_url(self):
        return "/%s/" % self.slug

    def get_breadcrumbs(self):
        nav = self.navigation_set.all()[0]
        trail = [nav]
        while nav.parent:
            nav = nav.parent
            trail.append(nav)
        return reversed(trail)

    def get_navigation_header(self):
        nav = self.navigation_set.all()[0]
        while nav.parent:
            nav = nav.parent
        return nav

    def get_other_navigation(self):
        return self.get_navigation_header().navigation_set.all().order_by('order')

    def __str__(self):
        return self.slug


class NavigationManager(models.Manager):
    def get_first(self):
        top_level_navs = self.filter(parent=None).order_by('order')
        if top_level_navs:
            return top_level_navs[0]


class Navigation(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    text = models.CharField(max_length=100)
    order = models.IntegerField()
    article = models.ForeignKey(Article, blank=True, null=True)

    objects = NavigationManager()

    def get_article(self):
        if self.article:
            return self.article
        else:
            for navigation in self.navigation_set.all():
                if navigation.article:
                    return navigation.article
                else:
                    return navigation.get_article()

    def get_top_parent(self):
        current = self
        while current.parent:
            current = current.parent
        return current

    def flatten(self, level=0):
        flat_list = [{'object': self, 'level': level}]
        if self.navigation_set.all():
            flat_list.append('begin-child')
        for child in self.navigation_set.all():
            flat_list += child.flatten(level + 1)
        if self.navigation_set.all():
            flat_list.append('end-child')
        return flat_list

    def __str__(self):
        return self.text

    def Meta(self):
        ordering = ['order',]
