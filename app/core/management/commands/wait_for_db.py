
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError



class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg20pError,OperationalError):
                self.stdout.write(self.style.WARNING('Databases unvailable, wait a second'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is available'))
