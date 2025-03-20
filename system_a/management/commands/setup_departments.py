from django.core.management.base import BaseCommand
from system_a.models import Department

class Command(BaseCommand):
    help = 'Creates initial departments'

    def handle(self, *args, **kwargs):
        departments = [
            {
                'name': 'Engineering',
                'description': 'Software development and technical operations'
            },
            {
                'name': 'Marketing',
                'description': 'Brand management and marketing operations'
            },
            {
                'name': 'HR',
                'description': 'Human resources and employee management'
            },
            {
                'name': 'Sales',
                'description': 'Sales and client relationships'
            }
        ]

        for dept in departments:
            Department.objects.get_or_create(
                name=dept['name'],
                defaults={'description': dept['description']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created department "{dept["name"]}"')
            ) 