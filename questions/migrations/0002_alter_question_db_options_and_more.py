# Generated by Django 4.0.2 on 2022-04-05 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question_db',
            options={'verbose_name_plural': 'Question DB'},
        ),
        migrations.AlterField(
            model_name='question_db',
            name='professor',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'PROFESSOR'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Question_Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qPaperTitle', models.CharField(max_length=100)),
                ('professor', models.ForeignKey(limit_choices_to={'groups__name': 'PROFESSOR'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(to='questions.Question_DB')),
            ],
        ),
    ]