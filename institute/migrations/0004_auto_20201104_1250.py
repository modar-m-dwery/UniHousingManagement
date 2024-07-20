# Generated by Django 3.0.6 on 2020-11-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0003_auto_20200923_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='bank',
            new_name='father_name',
        ),
        migrations.RemoveField(
            model_name='official',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='student',
            name='affidavit',
        ),
        migrations.RemoveField(
            model_name='student',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='student',
            name='application',
        ),
        migrations.RemoveField(
            model_name='student',
            name='challan_no',
        ),
        migrations.RemoveField(
            model_name='student',
            name='dop',
        ),
        migrations.RemoveField(
            model_name='student',
            name='has_paid',
        ),
        migrations.RemoveField(
            model_name='student',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='student',
            name='undertaking_form',
        ),
        migrations.AddField(
            model_name='student',
            name='mother_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='student',
            name='community',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='emergency_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]