from django.test import TestCase, Client
from django.urls import reverse
from django.template import Template, Context
from django.http import HttpRequest
from .models import MenuItem


class MenuTests(TestCase):
    def setUp(self):
        """
        Настройка тестовых данных: создание родительского и дочернего пунктов меню.
        """
        self.client = Client()
        self.parent = MenuItem.objects.create(
            title="Parent",
            url="home",
            menu_name="main_menu",
            order=1
        )
        self.child = MenuItem.objects.create(
            title="Child",
            url="/child",
            menu_name="main_menu",
            parent=self.parent,
            order=1
        )

    def test_menu_tree(self):
        """
        Проверяет, что get_menu_tree правильно определяет активный пункт и иерархию.
        """
        tree = MenuItem.get_menu_tree("main_menu", "/child")
        self.assertEqual(len(tree), 1)
        self.assertTrue(tree[0].is_ancestor)
        self.assertTrue(tree[0].children_list[0].is_active)

    def test_get_absolute_url(self):
        """
        Проверяет, что get_absolute_url возвращает правильный URL для named и явных URL.
        """
        self.assertEqual(self.parent.get_absolute_url(), reverse("home"))
        self.assertEqual(self.child.get_absolute_url(), "/child")

    def test_draw_menu(self):
        """
        Проверяет, что template tag draw_menu рендерит меню с активным пунктом.
        """
        # Создаем HttpRequest вручную
        request = HttpRequest()
        request.path = reverse("home")
        request.path_info = reverse("home")

        template = Template('{% load menu_tags %}{% draw_menu "main_menu" %}')
        context = Context({"request": request})
        rendered = template.render(context)
        self.assertIn("Parent", rendered)
        self.assertIn("active", rendered)