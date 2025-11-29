"""
Django management command to seed the database with sample services
Run this with: python manage.py seed_services
"""
from django.core.management.base import BaseCommand
from hospital_admin.models import Service


class Command(BaseCommand):
    help = 'Seeds the database with sample hospital services'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding services...')
        
        services_data = [
            {
                'name': 'Emergency Ambulance',
                'category': 'emergency',
                'description': '24/7 emergency ambulance service with trained paramedics and advanced life support equipment. Rapid response for critical medical situations.',
                'icon': 'fa-ambulance',
                'contact_number': '+880-1234-567890',
                'order': 1,
                'is_active': True,
            },
            {
                'name': 'General Consultation',
                'category': 'consultation',
                'description': 'Comprehensive health checkups and medical consultations with experienced general physicians. Get expert advice for your health concerns.',
                'icon': 'fa-user-md',
                'contact_number': '+880-1234-567891',
                'order': 2,
                'is_active': True,
            },
            {
                'name': 'Cardiology Department',
                'category': 'specialized',
                'description': 'Specialized cardiac care with advanced diagnostic facilities including ECG, ECHO, and cardiac catheterization. Expert cardiologists available.',
                'icon': 'fa-heartbeat',
                'contact_number': '+880-1234-567892',
                'order': 3,
                'is_active': True,
            },
            {
                'name': 'X-Ray & Imaging',
                'category': 'diagnostics',
                'description': 'Digital X-ray, CT scan, MRI, and ultrasound services with latest technology. Quick and accurate diagnostic imaging.',
                'icon': 'fa-x-ray',
                'contact_number': '',
                'order': 4,
                'is_active': True,
            },
            {
                'name': 'Clinical Laboratory',
                'category': 'laboratory',
                'description': 'Comprehensive diagnostic laboratory services including blood tests, urine tests, pathology, and microbiology. Results available quickly.',
                'icon': 'fa-microscope',
                'contact_number': '',
                'order': 5,
                'is_active': True,
            },
            {
                'name': 'Orthopedic Surgery',
                'category': 'specialized',
                'description': 'Advanced orthopedic care for bone, joint, and muscle problems. Expert surgeons and modern operation theaters.',
                'icon': 'fa-bone',
                'contact_number': '+880-1234-567893',
                'order': 6,
                'is_active': True,
            },
            {
                'name': 'Pediatrics',
                'category': 'consultation',
                'description': 'Specialized healthcare for infants, children, and adolescents. Child-friendly environment with experienced pediatricians.',
                'icon': 'fa-baby',
                'contact_number': '+880-1234-567894',
                'order': 7,
                'is_active': True,
            },
            {
                'name': 'Dental Care',
                'category': 'specialized',
                'description': 'Complete dental services including checkups, cleaning, fillings, root canal, and cosmetic dentistry.',
                'icon': 'fa-tooth',
                'contact_number': '+880-1234-567895',
                'order': 8,
                'is_active': True,
            },
            {
                'name': 'Maternity & Gynecology',
                'category': 'specialized',
                'description': "Women's health services including prenatal care, delivery, and gynecological consultations with female doctors.",
                'icon': 'fa-female',
                'contact_number': '+880-1234-567896',
                'order': 9,
                'is_active': True,
            },
            {
                'name': 'Pharmacy Services',
                'category': 'other',
                'description': '24/7 in-house pharmacy with a wide range of medications. Prescription drugs and over-the-counter medicines available.',
                'icon': 'fa-pills',
                'contact_number': '+880-1234-567897',
                'order': 10,
                'is_active': True,
            },
            {
                'name': 'ICU & Critical Care',
                'category': 'emergency',
                'description': 'Intensive Care Unit with advanced life support systems and 24/7 monitoring for critically ill patients.',
                'icon': 'fa-procedures',
                'contact_number': '+880-1234-567898',
                'order': 11,
                'is_active': True,
            },
            {
                'name': 'Physiotherapy',
                'category': 'other',
                'description': 'Rehabilitation services for physical injuries and post-surgery recovery. Expert physiotherapists and modern equipment.',
                'icon': 'fa-walking',
                'contact_number': '',
                'order': 12,
                'is_active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for service_data in services_data:
            service, created = Service.objects.update_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {service.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'→ Updated: {service.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Seeding complete!'))
        self.stdout.write(f'Created: {created_count} services')
        self.stdout.write(f'Updated: {updated_count} services')
        self.stdout.write(f'Total: {Service.objects.count()} services in database')
