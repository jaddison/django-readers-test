import random
import secrets

from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from data.models import Author, Book


class Command(BaseCommand):
    help = 'Prepopulate Authors and Books for testing purposes'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        fake = Faker()

        for n in range(100000):
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio="\n\n".join(fake.paragraphs(nb=3)),
                birthday=fake.date_of_birth(minimum_age=18)
            )

            Book.objects.bulk_create([
                Book(
                    author=author,
                    isbn=fake.isbn13(),
                    title=fake.sentence(nb_words=random.randrange(1, 5)).strip('.'),
                    subtitle=fake.sentence(nb_words=random.randrange(10, 30)).strip('.'),
                    snippet="\n\n".join(fake.paragraphs(nb=50)),
                    published=fake.date_between(),
                ) for m in range(secrets.randbelow(50))
            ])
