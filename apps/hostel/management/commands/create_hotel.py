from django.core.management.base import BaseCommand
from apps.hostel.models import Hotel
import uuid


class Command(BaseCommand):
    help = 'Creates a hotel instance interactively'

    def handle(self, *args, **options):
        # Check if hotel already exists
        if Hotel.objects.filter(is_deleted=False).exists():
            self.stdout.write(
                self.style.ERROR('A hotel already exists in the system. Only one hotel instance is allowed.')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('Hotel Creation Wizard')
        )
        self.stdout.write('=' * 50)
        self.stdout.write('(Press Enter to skip optional fields)\n')

        try:
            # Required field
            name = self._get_required_input('Hotel name: ')
            
            # Optional fields
            address = self._get_optional_input('Address: ')
            city = self._get_optional_input('City: ')
            country = self._get_optional_input('Country: ')
            postal_code = self._get_optional_input('Postal code: ')
            phone = self._get_optional_input('Phone: ')
            email = self._get_optional_input('Email: ')
            
            # Time fields with defaults
            check_in_input = input('Check-in time (HH:MM) [default: 14:00]: ').strip()
            check_in_time = check_in_input if check_in_input else '14:00'
            
            check_out_input = input('Check-out time (HH:MM) [default: 12:00]: ').strip()
            check_out_time = check_out_input if check_out_input else '12:00'

            # Validate time format
            try:
                from datetime import datetime
                datetime.strptime(check_in_time, '%H:%M')
                datetime.strptime(check_out_time, '%H:%M')
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid time format. Use HH:MM format.'))
                return

            # Auto-generate id_number
            id_number = str(uuid.uuid4())[:12]

            # Create hotel
            hotel = Hotel.objects.create(
                name=name,
                id_number=id_number,
                address=address or '',
                city=city or '',
                country=country or '',
                postal_code=postal_code or '',
                phone=phone or '',
                email=email or '',
                check_in_time=check_in_time,
                check_out_time=check_out_time,
            )

            self.stdout.write(
                self.style.SUCCESS('\n✓ Hotel created successfully!')
            )
            self.stdout.write(f'\nHotel Details:')
            self.stdout.write(f'  Name: {hotel.name}')
            self.stdout.write(f'  ID Number: {hotel.id_number}')
            self.stdout.write(f'  Address: {hotel.address}')
            self.stdout.write(f'  City: {hotel.city}')
            self.stdout.write(f'  Country: {hotel.country}')
            self.stdout.write(f'  Postal Code: {hotel.postal_code}')
            self.stdout.write(f'  Phone: {hotel.phone}')
            self.stdout.write(f'  Email: {hotel.email}')
            self.stdout.write(f'  Check-in: {hotel.check_in_time}')
            self.stdout.write(f'  Check-out: {hotel.check_out_time}')

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n\nHotel creation cancelled.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def _get_required_input(self, prompt):
        """Get required input from user"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            self.stdout.write(self.style.WARNING('This field is required. Please enter a value.'))

    def _get_optional_input(self, prompt):
        """Get optional input from user"""
        value = input(prompt).strip()
        return value if value else None
