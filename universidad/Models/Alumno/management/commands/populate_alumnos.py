from django.core.management.base import BaseCommand
from universidad.Models.Alumno.models import Alumno
from faker import Faker
import random

class Command(BaseCommand):
    help = "Poblar la base de datos con 10,000 alumnos falsos"

    def handle(self, *args, **kwargs):
        fake = Faker()
        alumnos = []
        genders = ["M", "F"]

        for i in range(10000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{i}@uni.com"
            phone = str(fake.random_number(digits=8, fix_len=True))
            gender = random.choice(genders)
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=30)
            ##carnet = str(fake.random_number(digits=10, fix_len=True))
            carnet = str(i).zfill(10)  # Genera un carné único basado en el índice y evitamos duplicados

            alumnos.append(
                Alumno(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    gender=gender,
                    birth_date=birth_date,
                    carnet=carnet
                )
            )

        Alumno.objects.bulk_create(alumnos)
        self.stdout.write(self.style.SUCCESS("Se crearon 10,000 alumnos"))
