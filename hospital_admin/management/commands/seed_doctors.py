"""
Django management command to seed the database with 50+ doctors
Run this with: python manage.py seed_doctors
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctor.models import DoctorProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with 50+ doctors'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding doctors...')

        specializations = [
            'Cardiologist', 'Dermatologist', 'Neurologist', 'Pediatrician',
            'Psychiatrist', 'Surgeon', 'Orthopedic', 'Gynecologist',
            'Oncologist', 'ENT Specialist', 'Dentist', 'Ophthalmologist',
            'Urologist', 'Endocrinologist', 'Gastroenterologist'
        ]

        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
            'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
            'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
            'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
            'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
            'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
            'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
            'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
            'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Gregory', 'Christine', 'Alexander', 'Debra'
        ]

        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
            'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
            'Carter', 'Roberts'
        ]

        # Generate 55 doctors to be safe
        for i in range(55):
            first = random.choice(first_names)
            last = random.choice(last_names)
            username = f"dr_{first.lower()}_{last.lower()}_{random.randint(100, 999)}"
            email = f"{username}@hospital.com"
            
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"dr_{first.lower()}_{last.lower()}_{random.randint(1000, 9999)}"
            
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=first,
                last_name=last,
                is_doctor=True
            )

            # Create Doctor Profile
            spec = random.choice(specializations)
            DoctorProfile.objects.create(
                user=user,
                specialization=spec,
                address=f"{random.randint(1, 999)} Medical Center Blvd, City",
                phone_number=f"+880-1{random.randint(3, 9)}-{random.randint(10000000, 99999999)}",
                status='active'  # Automatically active
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created Dr. {first} {last} ({spec})'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created 55 doctors!'))
