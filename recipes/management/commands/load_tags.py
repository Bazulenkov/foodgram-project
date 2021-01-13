"""
Import TAGS to Datababse
"""
from django.core.management.base import BaseCommand

from recipes.models import Tag

TAGS = {
    "breakfast": {"name": "Завтрак", "slug": "breakfast", "color": "orange"},
    "lunch": {"name": "Обед", "slug": "lunch", "color": "green"},
    "dinner": {"name": "Ужин", "slug": "dinner", "color": "purple"},
}


class Command(BaseCommand):
    def import_tags(self):
        for tag in TAGS:
            try:
                tag, created = Tag.objects.get_or_create(
                    name=TAGS[tag]['name'], slug=TAGS[tag]['slug'], color=TAGS[tag]['color']
                )
                if created:
                    tag.save()
                    display_format = "Tag, {}, has been saved."
                    print(display_format.format(tag))
                else:
                    print(f"Tag -{tag}- already exists")
            except Exception as ex:
                print(str(ex))
                msg = (
                    "\n\nSomething went wrong saving this tag: {}\n{}".format(
                        tag, str(ex)
                    )
                )
                print(msg)

    def handle(self, *args, **options):
        """Call the function to import data"""
        self.import_tags()