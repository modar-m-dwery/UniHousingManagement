# Generated by Django 3.0.6 on 2020-09-23 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_email', models.EmailField(max_length=254, unique=True)),
                ('regd_no', models.CharField(max_length=20, unique=True)),
                ('roll_no', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('branch', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('ECE', 'Electronics and Communication Engineering'), ('EEE', 'Electrical and Electronics Engineering'), ('CHE', 'Chemical Engineering'), ('MME', 'Metallurgical and Materials Engineering'), ('MEC', 'Mechanical Engineering'), ('CIV', 'Civil Engineering'), ('BIO', 'Biotechnology')], max_length=3)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=7)),
                ('pwd', models.BooleanField(default=False)),
                ('community', models.CharField(choices=[('GEN', 'GEN'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'), ('EWS', 'EWS')], max_length=25)),
                ('year', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('dob', models.DateField()),
                ('blood_group', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=10)),
                ('parents_phone', models.CharField(max_length=10)),
                ('emergency_phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('photo', models.FileField(blank=True, null=True, upload_to='')),
                ('is_hosteller', models.BooleanField(default=True)),
                ('has_paid', models.BooleanField(default=False, null=True)),
                ('amount_paid', models.FloatField(blank=True, default=0, null=True)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('challan_no', models.CharField(blank=True, max_length=64, null=True)),
                ('dop', models.DateField(blank=True, null=True)),
                ('application', models.FileField(blank=True, null=True, upload_to='')),
                ('undertaking_form', models.FileField(blank=True, null=True, upload_to='')),
                ('receipt', models.FileField(blank=True, null=True, upload_to='')),
                ('affidavit', models.FileField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Official',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_email', models.EmailField(max_length=254, unique=True)),
                ('emp_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(choices=[('Caretaker', 'Caretaker'), ('Warden', 'Warden'), ('Deputy Chief-Warden', 'Deputy Chief-Warden'), ('Chief-Warden', 'Chief-Warden')], max_length=20)),
                ('branch', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('ECE', 'Electronics and Communication Engineering'), ('EEE', 'Electrical and Electronics Engineering'), ('CHE', 'Chemical Engineering'), ('MME', 'Metallurgical and Materials Engineering'), ('MEC', 'Mechanical Engineering'), ('CIV', 'Civil Engineering'), ('BIO', 'Biotechnology'), ('SOS', 'School of Sciences'), ('SHM', 'School of Humanities and Management')], max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('room_type', models.CharField(choices=[('1S', 'One student per Room'), ('2S', 'Two students per Room'), ('4S', 'Four students per Room')], max_length=2)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=7)),
                ('capacity', models.IntegerField()),
                ('caretaker', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institute.Official')),
            ],
        ),
    ]
