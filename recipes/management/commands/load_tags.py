"""
Import TAGS to Datababse
"""
from django.core.management.base import BaseCommand

from recipes.models import Tag

TAGS = ["Завтрак", "Обед", "Ужин"]

class Command(BaseCommand):
    def import_tags(self):
        for tag_name in TAGS:
            try:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                if created:
                    tag.save()
                    display_format = "\nTag, {}, has been saved."
                    print(display_format.format(tag))
            except Exception as ex:
                print(str(ex))
                msg = "\n\nSomething went wrong saving this tag: {}\n{}".format(tag_name, str(ex))
                print(msg)
    
    def handle(self, *args, **options):
        """Call the function to import data"""
        self.import_tags()