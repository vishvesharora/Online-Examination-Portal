# Generated by Django 4.0.2 on 2022-03-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_studentinfo_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='branch',
            field=models.CharField(choices=[('CSE', 'Computer Science Eng'), ('ECE', 'Electrical Eng'), ('CE', 'Civil Eng'), ('ME', 'Mechanical Eng')], max_length=3),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
