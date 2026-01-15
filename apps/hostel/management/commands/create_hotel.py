from django.core.management.base import BaseCommand
from apps.hostel.models import Hotel, Setting
from apps.users.models import User
from django.contrib.auth.models import Group
from utils.enums import GroupNames
import uuid


class Command(BaseCommand):
    help = 'Creates a hotel instance, admin user, admin group, and settings interactively'

    def handle(self, *args, **options):
        # Check if hotel already exists
        if Hotel.objects.filter(is_deleted=False).exists():
            self.stdout.write(
                self.style.ERROR('A hotel already exists in the system. Only one hotel instance is allowed.')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('Hotel Setup Wizard')
        )
        self.stdout.write('=' * 50)
        self.stdout.write('(Press Enter to skip optional fields)\n')

        try:
            # Step 1: Create or get Admin Group
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(self.style.HTTP_INFO('STEP 1: Setting up Admin Group'))
            self.stdout.write('=' * 50)
            admin_group, group_created = Group.objects.get_or_create(name=GroupNames.ADMIN.value)
            staff_group, staff_group_created = Group.objects.get_or_create(name=GroupNames.STAFF.value)
            if group_created:
                self.stdout.write(self.style.SUCCESS('✓ Admin group created'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ Admin group already exists'))
            if staff_group_created:
                self.stdout.write(self.style.SUCCESS('✓ Staff group created'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ Staff group already exists'))

            # Step 2: Create Hotel
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(self.style.HTTP_INFO('STEP 2: Hotel Information'))
            self.stdout.write('=' * 50)
            
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

            self.stdout.write(self.style.SUCCESS('✓ Hotel created successfully!'))
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

            # Step 3: Create Admin Account
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(self.style.HTTP_INFO('STEP 3: Create Admin Account'))
            self.stdout.write('=' * 50)
            
            admin_username = self._get_required_input('Admin username: ')
            
            # Check if admin user already exists
            if User.objects.filter(username=admin_username).exists():
                self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists. Skipping admin creation.'))
            else:
                admin_password = self._get_required_password('Admin password: ')
                admin_password_confirm = self._get_required_password('Confirm password: ')
                
                if admin_password != admin_password_confirm:
                    self.stdout.write(self.style.ERROR('Passwords do not match!'))
                    return
                
                # Create admin user using the manager style
                admin_user = User.objects.create_superuser(
                    username=admin_username,
                    password=admin_password,
                    is_active=True
                )
                
                # Add admin user to Admin group
                admin_user.groups.add(admin_group)
                
                self.stdout.write(self.style.SUCCESS('✓ Admin account created successfully!'))
                self.stdout.write(f'  Username: {admin_user.username}')
                self.stdout.write(f'  ✓ Added to Admin group')

            # Step 4: Create Settings
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(self.style.HTTP_INFO('STEP 4: Configure Settings'))
            self.stdout.write('=' * 50)
            
            if Setting.objects.filter(is_deleted=False).exists():
                self.stdout.write(self.style.SUCCESS('✓ Settings already exist'))
            else:
                try:
                    tax_input = input('Tax percentage [default: 0]: ').strip()
                    tax_percentage = float(tax_input) if tax_input else 0
                except ValueError:
                    self.stdout.write(self.style.WARNING('Invalid tax input. Using default 0%'))
                    tax_percentage = 0
                
                try:
                    discount_input = input('Default discount percentage [default: 0]: ').strip()
                    discount_percentage = float(discount_input) if discount_input else 0
                except ValueError:
                    self.stdout.write(self.style.WARNING('Invalid discount input. Using default 0%'))
                    discount_percentage = 0
                
                setting = Setting.objects.create(
                    tax_percentage=tax_percentage,
                    default_discount_percentage=discount_percentage,
                    description='Default settings created during hotel setup'
                )
                self.stdout.write(self.style.SUCCESS('✓ Settings created successfully!'))
                self.stdout.write(f'  Tax: {setting.tax_percentage}%')
                self.stdout.write(f'  Discount: {setting.default_discount_percentage}%')

            # Final Summary
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(self.style.SUCCESS('✓ HOTEL SETUP COMPLETED SUCCESSFULLY!'))
            self.stdout.write('=' * 50)
            self.stdout.write('\nSummary:')
            self.stdout.write(f'  ✓ Hotel: {hotel.name}')
            self.stdout.write(f'  ✓ Admin Group: {GroupNames.ADMIN.value}')
            self.stdout.write(f'  ✓ Admin User: {admin_username}')
            self.stdout.write(f'  ✓ Settings: Configured')
            self.stdout.write('\nYou can now log in with your admin credentials.')

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n\nSetup cancelled.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()

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
    
    def _get_required_password(self, prompt):
        """Get required password input from user (hidden)"""
        import getpass
        while True:
            password = getpass.getpass(prompt)
            if password:
                return password
            self.stdout.write(self.style.WARNING('Password cannot be empty. Please enter a value.'))
