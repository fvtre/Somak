# Generated by Django 5.1.2 on 2024-12-02 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('home', 'Home'), ('casadepaz', 'Casa de Paz'), ('aviva2', 'Aviva2'), ('avivakids', 'Avivakids'), ('jovenes', 'Jovenes')], default='', max_length=20),
        ),
    ]
