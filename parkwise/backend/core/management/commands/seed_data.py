from django.core.management.base import BaseCommand

from core.seed import load_seed_data


class Command(BaseCommand):
    help = "Create the 40 slots (20 per gate) and clear all visits and payments."

    def handle(self, *args, **options):
        load_seed_data()
        self.stdout.write(self.style.SUCCESS("Slots ready, lot is empty."))
