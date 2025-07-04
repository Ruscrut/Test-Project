# Django-меню с древовидной структурой

Это простое Django-приложение для отображения многоуровневого меню на сайте.

## Возможности

- Меню хранится в базе данных.
- Управляется через стандартную админку Django.
- Поддержка вложенности (родитель → потомки).
- Активный пункт определяется по URL страницы.
- Первый уровень вложенности под активным пунктом также раскрывается.
- Поддержка нескольких меню по названию (например: `main_menu`, `footer_menu` и т.д.).
- URL может быть обычным (`/about/`) или именованным (`home`).
- Ровно **один** SQL-запрос на отрисовку меню.
- Используется template tag:  
  ```django
  {% draw_menu 'main_menu' %}
  ```

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your_username/menu_project.git
   cd menu_project
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Примените миграции:
   ```bash
   python manage.py migrate
   ```

4. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

5. Перейдите в админку (`/admin/`) и создайте меню и пункты меню.

## Использование

Вставьте тег меню в нужное место шаблона:

```django
{% load menu_tags %}
{% draw_menu 'main_menu' %}
```

Меню будет отрисовано с учетом текущего URL и иерархии.

## Ограничения

- Только Django и стандартная библиотека Python.
- Меню отображается на основе шаблона `menu/menu_tree.html`.
- JavaScript и CSS уже подключены.

---

Проект выполнен в учебных целях.
