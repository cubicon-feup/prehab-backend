# Generated by Django 2.0.2 on 2018-04-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConstraintType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'constraint_type',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorPatient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'doctor_patient',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PatientConstraintType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('constraint_type', models.ForeignKey(db_column='constraint_type_id',
                                                      on_delete=django.db.models.deletion.CASCADE, to='prehab_app.ConstraintType')),
            ],
            options={
                'db_table': 'patient_constraint_type',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PatientTaskSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('week_number', models.IntegerField()),
                ('day_number', models.IntegerField()),
                ('expected_repetitions', models.IntegerField(null=True)),
                ('actual_repetitions', models.IntegerField(null=True)),
                ('status', models.IntegerField(default=1, null=True)),
            ],
            options={
                'db_table': 'patient_task_schedule',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Prehab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('init_date', models.DateField()),
                ('expected_end_date', models.DateField()),
                ('actual_end_date', models.DateField()),
                ('surgery_date', models.DateField()),
                ('week_number', models.IntegerField()),
            ],
            options={
                'db_table': 'prehab',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PrehabStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'prehab_status',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'role',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleWeekTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('week_number', models.IntegerField()),
            ],
            options={
                'db_table': 'schedule_week_task',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=512, null=True)),
                ('multimedia_link', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'task',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'task_schedule',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskScheduleStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'task_schedule_status',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
            options={
                'db_table': 'task_type',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, null=True)),
                ('email', models.CharField(max_length=64, null=True)),
                ('phone', models.CharField(max_length=64, null=True)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=64, null=True)),
                ('activation_code', models.CharField(max_length=8)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE,
                                            primary_key=True, serialize=False, to='prehab_app.User')),
                ('department', models.CharField(max_length=64, null=True)),
            ],
            options={
                'db_table': 'doctor',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE,
                                            primary_key=True, serialize=False, to='prehab_app.User')),
                ('patient_tag', models.CharField(max_length=16)),
                ('age', models.IntegerField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('sex', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'patient',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(db_column='role_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Role'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(db_column='task_type_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.TaskType'),
        ),
        migrations.AddField(
            model_name='scheduleweektask',
            name='task',
            field=models.ForeignKey(db_column='task_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Task'),
        ),
        migrations.AddField(
            model_name='scheduleweektask',
            name='task_schedule',
            field=models.ForeignKey(db_column='task_schedule_id', on_delete=django.db.models.deletion.CASCADE,
                                    to='prehab_app.TaskSchedule'),
        ),
        migrations.AddField(
            model_name='prehab',
            name='status',
            field=models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.PrehabStatus'),
        ),
        migrations.AddField(
            model_name='patienttaskschedule',
            name='prehab',
            field=models.ForeignKey(db_column='prehab_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Prehab'),
        ),
        migrations.AddField(
            model_name='patienttaskschedule',
            name='task',
            field=models.ForeignKey(db_column='task_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Task'),
        ),
        migrations.AddField(
            model_name='taskschedule',
            name='created_by',
            field=models.ForeignKey(db_column='doctor_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Doctor'),
        ),
        migrations.AddField(
            model_name='patientconstrainttype',
            name='patient',
            field=models.ForeignKey(db_column='patient_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Patient'),
        ),
        migrations.AddField(
            model_name='doctorpatient',
            name='doctor',
            field=models.ForeignKey(db_column='doctor_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Doctor'),
        ),
        migrations.AddField(
            model_name='doctorpatient',
            name='patient',
            field=models.ForeignKey(db_column='patient_id', on_delete=django.db.models.deletion.CASCADE, to='prehab_app.Patient'),
        ),
    ]
