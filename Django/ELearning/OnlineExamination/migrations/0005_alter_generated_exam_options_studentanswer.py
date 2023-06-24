# Generated by Django 4.1 on 2023-06-15 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineExamination', '0004_alter_studentexam_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generated_exam',
            options={'ordering': ['-date_created'], 'verbose_name': 'Examination Generated'},
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answers', models.TextField()),
                ('marks_scored', models.BigIntegerField(default=0)),
                ('is_marked_byML', models.BooleanField(default=False)),
                ('is_verified_teacher', models.BooleanField(default=False)),
                ('generated_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineExamination.generated_exam')),
                ('studentExam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineExamination.studentexam')),
            ],
            options={
                'verbose_name': 'Student Answer',
                'db_table': 'Student Answer',
            },
        ),
    ]
