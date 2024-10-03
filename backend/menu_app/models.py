from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "main_menu"
        verbose_name = "Главное меню"
        verbose_name_plural = "Главное меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    named_url = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        db_table = "item_menu"
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.title

    # Для показа, ниже приведен пример сырого SQL запроса:

    # @classmethod
    # def get_menu_with_items(cls, menu_name):
    #     query = '''
    #     SELECT 
    #         menuitem.id AS id,
    #         menuitem.title AS title,
    #         menuitem.url AS url,
    #         menuitem.named_url AS named_url,
    #         menuitem.parent_id AS parent_id
    #     FROM
    #         menu_item AS menuitem
    #     JOIN
    #         menu AS m ON menuitem.menu_id = m.id
    #     WHERE
    #         m.name = %s;
    #     '''
    #     return cls.objects.raw(query, [menu_name])