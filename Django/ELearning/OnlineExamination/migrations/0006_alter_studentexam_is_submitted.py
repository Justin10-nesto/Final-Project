# Generated by Django 4.1 on 2023-06-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineExamination', '0005_alter_generated_exam_options_studentanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentexam',
            name='is_submitted',
            field=models.BooleanField(default=True),
        ),
    ]