from .shoplist import ShopList


class ShopListMixin:
    """Добавляет в context shoplist."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoplist = ShopList(self.request)
        context["shoplist"] = shoplist.shoplist
        return context
