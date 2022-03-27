# Generated by Django 2.0.1 on 2018-01-28 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    jobs = [('TEACHER', 'Teacher'), ('STUDENT', 'Student'), ('PROGRAMMER', 'Programmer'),
            ('ARTIST', 'Artist'), ('MANAGER', 'Manager'), ('ARMY', 'Army'),
            ('POLICE', 'Police'), ('DOCTOR', 'Doctor'), ('VET', 'Vet'),
            ('NURSE', 'Nurse'), ('TECHNICHIAN', 'Technichian'),
            ('CLEANER', 'Cleaner'), ('OTHER', 'Other'), ('UNEMPLOYED', 'Unemployed')]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[]
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('house_id', models.IntegerField(default=0, primary_key=True, serialize=False,
                                                 validators=[django.core.validators.MinValueValidator(0)])),
                ('name', models.CharField(max_length=100)),
                ('public', models.BooleanField(default=False)),
                ('city', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='house.City')),
                ('country', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='house.Country')),
                ('parent_profession_1', models.CharField(
                    max_length=50, choices=jobs)),
                ('parent_profession_2', models.CharField(
                    max_length=50, choices=jobs)),
                ('income', models.IntegerField(blank=True, null=True)),
                ('children', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='house.Country'),
        ),
    ]
