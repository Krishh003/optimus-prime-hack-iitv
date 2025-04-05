# Generated by Django 3.1.12 on 2025-04-05 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_clientlisting_user_alter_sponsorlisting_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_no', models.CharField(max_length=15)),
                ('avg_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('state', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'colleges',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_no', models.CharField(max_length=15)),
                ('avg_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sponsors',
            },
        ),
        migrations.AlterField(
            model_name='clientlisting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sponsorlisting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='SponsorHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField()),
                ('event_type', models.CharField(choices=[('sponsor_event', 'Sponsor Event'), ('college_event', 'College Event')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.college')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.sponsor')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('keywords', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.sponsor')),
            ],
            options={
                'db_table': 'sponsor_events',
            },
        ),
        migrations.CreateModel(
            name='EventRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField()),
                ('event_type', models.CharField(choices=[('sponsor_event', 'Sponsor Event'), ('college_event', 'College Event')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_deliverables', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.college')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.sponsor')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeSponsorshipHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField()),
                ('event_type', models.CharField(choices=[('sponsor_event', 'Sponsor Event'), ('college_event', 'College Event')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.college')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.sponsor')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('contact_no', models.CharField(max_length=15)),
                ('basic_deliverables', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.college')),
            ],
            options={
                'db_table': 'college_events',
            },
        ),
    ]
