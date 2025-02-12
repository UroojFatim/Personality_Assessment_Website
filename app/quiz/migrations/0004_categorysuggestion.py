# Generated by Django 5.1.4 on 2024-12-28 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_result_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_marks', models.IntegerField()),
                ('end_marks', models.IntegerField()),
                ('suggestion', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestions', to='quiz.category')),
            ],
        ),
    ]
