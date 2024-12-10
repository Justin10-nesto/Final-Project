# Generated by Django 4.2.3 on 2023-07-11 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announciment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('is_opened', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Announciment',
                'db_table': 'Announciment',
            },
        ),
        migrations.CreateModel(
            name='AnnouncimentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Announciment Type',
                'db_table': 'Announciment Type',
            },
        ),
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('task', models.TextField(null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('Weight', models.IntegerField()),
                ('is_questions_exacted', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to='Assigments')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
            ],
            options={
                'verbose_name': 'Assigment',
                'db_table': 'Assigment',
            },
        ),
        migrations.CreateModel(
            name='AssigmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('weight', models.BigIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Assigment Type',
                'db_table': 'Assigment Type',
            },
        ),
        migrations.CreateModel(
            name='GroupDiscussionReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
            ],
            options={
                'verbose_name': 'Group Discussion Reply',
                'verbose_name_plural': 'Group Discussion Replies',
                'db_table': 'Group Discussion Reply',
            },
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('has_topic', models.BooleanField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Group Post',
                'db_table': 'Group Post',
            },
        ),
        migrations.CreateModel(
            name='GroupWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_description', models.TextField()),
            ],
            options={
                'verbose_name': 'Group Work',
                'verbose_name_plural': 'Group pWorks',
                'db_table': 'Group Work',
            },
        ),
        migrations.CreateModel(
            name='GroupWorkDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('comment', models.TextField(null=True)),
                ('presentation_date', models.DateTimeField()),
                ('is_presented', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Group Work Division',
                'db_table': 'Group Work Division',
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Question Type',
                'db_table': 'Question Type',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
                'db_table': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('registration_no', models.CharField(max_length=50)),
                ('index_number', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('school', models.CharField(max_length=255)),
                ('photo', models.FileField(null=True, upload_to='Photos')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('anaunciment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.announciment')),
                ('classCurrent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.studentclass')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.course')),
            ],
            options={
                'verbose_name': 'Student',
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('token', models.CharField(max_length=255, null=True)),
                ('file', models.FileField(null=True, upload_to='Groups')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
            ],
            options={
                'verbose_name': 'Student Group',
                'db_table': 'Student Group',
                'permissions': (('can_view_description', 'can view group description'), ('can_hide_description', 'can hide group description')),
            },
        ),
        migrations.CreateModel(
            name='StudentGroupManyToMany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.student')),
            ],
            options={
                'db_table': 'Group Members',
                'permissions': (('can_join_group', 'can join to the group'), ('can_left_group', 'can left from the group'), ('can_add_group_members', 'can add group members'), ('can_remove_group_members', 'can remove group members')),
                'default_permissions': ('add',),
            },
        ),
        migrations.CreateModel(
            name='StudentGroupType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Student Group Type',
                'db_table': 'Student Group Type',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subjectclass')),
            ],
            options={
                'verbose_name': 'Topic',
                'db_table': 'Topic',
            },
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('file', models.FileField(upload_to='Tutorials')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic')),
            ],
            options={
                'verbose_name': 'Tutorial',
                'db_table': 'Tutorial',
            },
        ),
        migrations.CreateModel(
            name='TutorialTimeTacking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.FloatField()),
                ('full_length', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.tutorial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('school', models.CharField(max_length=255)),
                ('photo', models.FileField(null=True, upload_to='Photos')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('anaunciment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.announciment')),
                ('classSubject', models.ManyToManyField(to='schools.subjectclass')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.department')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_presented', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('groupStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroupmanytomany')),
                ('work', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.groupworkdivision')),
            ],
            options={
                'db_table': 'Group and Student Task',
            },
        ),
        migrations.CreateModel(
            name='StudentSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('classCurrent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.studentclass')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
            ],
            options={
                'verbose_name': 'Student Subject',
                'db_table': 'Student Subject',
                'permissions': (('can_register_subject', 'can register subject'), ('can_deregister_subject', 'can deregister from a given subject subject'), ('can_remove_student_from_given_subject', 'can remove student from given subject'), ('can_add_studen_to_given_subject', 'can_add_studen_to_given_subject')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='type_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgrouptype'),
        ),
        migrations.CreateModel(
            name='StudentClassManyToMany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('classCurrent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.studentclass')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.student')),
            ],
            options={
                'db_table': 'Student Class',
                'permissions': (('can_promote_student', 'can promote student'), ('can_update_student_current_status', 'can update student current status'), ('can_track_and_evaluate_students', 'can track and evaluate students')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.questiontype')),
            ],
            options={
                'verbose_name': 'Question',
                'db_table': 'Question',
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('is_used', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OtpCode',
                'db_table': 'OtpCode',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('content', models.TextField(null=True)),
                ('is_questions_exacted', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to='Notes')),
                ('html', models.FileField(null=True, upload_to='NotesHtml')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic')),
            ],
            options={
                'verbose_name': 'Notes',
                'verbose_name_plural': 'Notes',
                'db_table': 'Notes',
            },
        ),
        migrations.AddField(
            model_name='groupworkdivision',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup'),
        ),
        migrations.AddField(
            model_name='groupworkdivision',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupworkdivision',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.student'),
        ),
        migrations.AddField(
            model_name='groupworkdivision',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.groupwork'),
        ),
        migrations.CreateModel(
            name='GroupPostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('message_liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.grouppost')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group Post Like',
                'db_table': 'Group Post Like',
            },
        ),
        migrations.CreateModel(
            name='GroupPostComent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.grouppost')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group Post Coment',
                'db_table': 'Group Post Coment',
            },
        ),
        migrations.AddField(
            model_name='grouppost',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup'),
        ),
        migrations.AddField(
            model_name='grouppost',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grouppost',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject'),
        ),
        migrations.AddField(
            model_name='grouppost',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic'),
        ),
        migrations.CreateModel(
            name='GroupDiscussionsMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_replay', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.groupdiscussionreply')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic')),
            ],
            options={
                'verbose_name': 'Group Discussions Message',
                'db_table': 'Group Discussions Message',
            },
        ),
        migrations.AddField(
            model_name='groupdiscussionreply',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic'),
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
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.schoollevel')),
            ],
            options={
                'verbose_name': 'Default Users',
                'db_table': 'Default Users',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('file', models.FileField(upload_to='Books')),
                ('is_questions_exacted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic')),
            ],
            options={
                'verbose_name': 'Book',
                'db_table': 'Book',
                'permissions': (('can_download', 'Can download book'), ('can_share_book', 'Can share book')),
            },
        ),
        migrations.CreateModel(
            name='AssigmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(null=True, upload_to='Submited Assigments')),
                ('parlagrims', models.IntegerField(default=0)),
                ('marks', models.IntegerField(default=0)),
                ('remark', models.CharField(max_length=255, null=True)),
                ('is_group', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('assigniment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.assigment')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.studentgroup')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Assigment Submission',
                'db_table': 'Assigment Submission',
                'permissions': (('can_submit_assigment', 'can can submit assigment'), ('can_view_submitted_assigment', 'can view submitted assigment'), ('can_resubmit_assigment', 'can resubmit assigment'), ('can_assign_marks', 'can assign marks and give comment to the assigment')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='assigment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic'),
        ),
        migrations.AddField(
            model_name='assigment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.assigmenttype'),
        ),
        migrations.AddField(
            model_name='announciment',
            name='announcimentType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.announcimenttype'),
        ),
        migrations.AddField(
            model_name='announciment',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announciment',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.subject'),
        ),
        migrations.AddField(
            model_name='announciment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineLearning.topic'),
        ),
    ]