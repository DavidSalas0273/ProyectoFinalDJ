from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Carga los datos iniciales de categorías, proveedores y productos de ejemplo.'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        call_command('loaddata', 'datos_iniciales.json', verbosity=0)
        self.stdout.write(self.style.SUCCESS(
            'Datos iniciales cargados correctamente: categorías, proveedores y productos.'
        ))
