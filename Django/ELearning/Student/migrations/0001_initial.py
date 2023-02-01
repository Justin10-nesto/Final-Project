# Generated by Django 4.1.3 on 2023-01-31 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('comment', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssigmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('weight', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DefaultUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('school_selected', models.TextField()),
                ('course', models.TextField()),
                ('type', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'DefaultUsers',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('content', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotesFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_of_documment', models.CharField(max_length=50)),
                ('type_of_the_book', models.CharField(max_length=50)),
                ('documment', models.FileField(upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroupType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'StudentGroupType',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=50)),
                ('subject_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('marks', models.BigIntegerField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.notesfiles')),
                ('notes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.notes')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.subject')),
            ],
        ),
        migrations.CreateModel(
            name='SubTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('marks', models.BigIntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.topics')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('assignent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.assigment')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.subject')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.studentgrouptype')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('registration_no', models.CharField(max_length=50)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.studentgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.questiontype')),
            ],
        ),
        migrations.AddField(
            model_name='assigment',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.status'),
        ),
        migrations.AddField(
            model_name='assigment',
            name='subtopic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Student.subtopic'),
        ),
        migrations.AddField(
            model_name='assigment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.assigmenttype'),
        ),
    ]
