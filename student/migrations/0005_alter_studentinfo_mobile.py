# Generated by Django 4.0.2 on 2022-03-30 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_studentinfo_branch_alter_studentinfo_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
    ]
