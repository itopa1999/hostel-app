from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates default user groups'

    def handle(self, *args, **options):
        # Define groups and their permissions
        groups_data = {
            'Admin': Permission.objects.all(),
            'Manager': Permission.objects.filter(
                codename__in=['add_user', 'change_user', 'delete_user', 'view_user']
            ),
            'Staff': Permission.objects.filter(
                codename__in=['view_user']
            ),
            'User': Permission.objects.filter(
                codename__in=['view_user']
            ),
        }

        for group_name, permissions in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(permissions)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created group "{group_name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group "{group_name}" already exists, permissions updated')
                )

        self.stdout.write(self.style.SUCCESS('All groups created successfully!'))
