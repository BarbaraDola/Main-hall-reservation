from django.core.management import BaseCommand
from reservation_app.models import MainHall

models_data = [
    {
        'name': 'A',
        'room_capacity': '10',
        'projector': 'False'
    },
{
        'name': 'B',
        'room_capacity': '20',
        'projector': 'True'
    },
{
        'name': 'C',
        'room_capacity': '35',
        'projector': 'False'
    },
{
        'name': 'D',
        'room_capacity': '50',
        'projector': 'True'
    },
{
        'name': 'E',
        'room_capacity': '100',
        'projector': 'True'
    },
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model_data in models_data:
            hall = MainHall.objects.create(**model_data)
            print(f'Sala {hall.name} - Added with room capacity: {hall.room_capacity}, '
                  f'projector availability: {hall.projector}')