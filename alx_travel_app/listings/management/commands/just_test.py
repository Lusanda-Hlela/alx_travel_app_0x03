"""My first custom made command just playing around."""
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1, type=str)
    
    def handle(self, *args, **options):
        name = options['username']
        if args:
            self.stdout.write(f'{args}')
        self.stdout.write(f'hello {name} nice to meet you')