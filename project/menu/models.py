from django.db import models
from django.urls import reverse, resolve, Resolver404
from django.core.exceptions import ValidationError

class MenuItem(models.Model):
    """
    Модель элемента меню.
    Хранит название, URL, родительский элемент и название меню для группировки.
    """
    title = models.CharField(
        max_length=255,
        verbose_name="Название пункта меню",
        help_text="Отображаемое название пункта меню"
    )
    url = models.CharField(
        max_length=255,
        verbose_name="URL",
        help_text="URL или named URL для перехода"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительский пункт",
        help_text="Родительский пункт меню для вложенности"
    )
    menu_name = models.CharField(
        max_length=100,
        verbose_name="Название меню",
        help_text="Название группы меню (например, 'main_menu')"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Порядок отображения пункта в меню"
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ['order', 'title']

    def str(self):
        return self.title

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для пункта меню.
        Если URL является named URL, пытается его разрешить, иначе возвращает как есть.
        """
        try:
            return reverse(self.url)
        except:
            return self.url

    @classmethod
    def get_menu_tree(cls, menu_name, current_url):
        """
        Получает дерево меню для указанного menu_name с учетом активного URL.
        Выполняет ровно один запрос к БД.
        """
        # Получаем все элементы меню с указанным menu_name
        items = cls.objects.filter(menu_name=menu_name).select_related('parent').order_by('order')
        
        # Инициализируем карту элементов и добавляем children_list
        item_map = {}
        for item in items:
            item_map[item.id] = item
            item.children_list = []  # Явная инициализация children_list для каждого объекта
        
        # Находим корневые элементы и строим дерево
        root_items = []
        for item in items:
            if item.parent_id is None:
                root_items.append(item)
            elif item.parent_id in item_map:
                item_map[item.parent_id].children_list.append(item)
            # Инициализируем флаги для всех элементов
            item.is_active = False
            item.is_ancestor = False
            item.is_child_of_active = False

        # Определяем активный элемент
        active_item = None
        for item in items:
            if item.get_absolute_url() == current_url:
                active_item = item
                break
            try:
                resolved = resolve(current_url)
                if item.get_absolute_url() == current_url or item.get_absolute_url() == f"/{resolved.url_name}/":
                    active_item = item
                    break
            except Resolver404:
                continue

        # Обновляем флаги для активного элемента и его предков
        if active_item:
            current = active_item
            while current:
                current.is_active = True
                current.is_ancestor = True
                for child in current.children_list:
                    child.is_child_of_active = True
                if current.parent_id and current.parent_id in item_map:
                    current = item_map[current.parent_id]
                else:
                    break

        return root_items

    def clean(self):
        if self.parent_id == self.id:
            raise ValidationError("Пункт меню не может быть родителем самого себя.")
        # Проверка на циклические зависимости
        seen = set()
        current = self.parent
        while current:
            if current.id in seen:
                raise ValidationError("Обнаружена циклическая зависимость в родительских пунктах.")
            seen.add(current.id)
            current = current.parent