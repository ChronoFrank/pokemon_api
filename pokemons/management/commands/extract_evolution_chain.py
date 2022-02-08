from django.core.management.base import BaseCommand, CommandError
from pokemons.tasks import evolution_chain_crawler

class Command(BaseCommand):
    help = 'This command receives a chain-id number and go to the pokeapi.co do download information\n' \
           'about the pokemons in that evolution chain representation'

    def add_arguments(self, parser):
        parser.add_argument('chain-id', type=int, help='A number between 1 and 467')

    def handle(self, *args, **options):
        if isinstance(options['chain-id'], int) and int(options['chain-id']) in range(1, 468):
            self.stdout.write(self.style.SUCCESS("extracting evolution chain "
                                                 "and pokemon information for id {0}".format(options['chain-id'])))
            try:
                evolution_chain_crawler(options['chain-id'])
            except Exception:
                raise CommandError('Evolution chain data not available for the id {0}'.format(options['chain-id']))

        else:
            raise CommandError('chain-id must be a number between 1 and 467')
