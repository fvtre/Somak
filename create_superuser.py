import os
import django

# Configura Django manualmente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Somak.settings")  # Reemplaza 'Somak' con el nombre de tu proyecto
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
SUPERUSER_EMAIL = "adrianoduque3@gmail.com"  # Cambia esto
SUPERUSER_PASSWORD = "ksmilesomak"  # Cambia esto

# Verifica si el superusuario ya existe
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print("Superusuario creado exitosamente.")
else:
    print("El superusuario ya existe.")
