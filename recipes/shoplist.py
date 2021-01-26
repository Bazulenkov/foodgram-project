from django.conf import settings


class ShopList:
    """Список рецептов(покупок)."""

    def __init__(self, request) -> None:
        """ Инициализация объекта списка покупок """
        self.session = request.session
        shoplist = self.session.get(settings.SHOPLIST_SESSION_ID)
        if not shoplist:
            # Сохраняем в сессии пустой список
            shoplist = self.session[settings.SHOPLIST_SESSION_ID] = []
        self.shoplist = shoplist

    def save(self):
        """ Помечаем сессию как измененную """
        self.session.modified = True

    def add(self, recipe_id: int):
        """ Добавление рецепта в список """

        if recipe_id not in self.shoplist:
            self.shoplist.append(recipe_id)
            self.save()

    def remove(self, recipe_id: int):
        """ Удаление товара из корзины """
        if recipe_id in self.shoplist:
            self.shoplist.remove(recipe_id)
            self.save()
