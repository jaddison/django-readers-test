# Generated by Django 3.2.16 on 2022-11-05 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=100)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('bio', models.TextField(blank=True, default='')),
                ('birthday', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('isbn', models.CharField(blank=True, db_index=True, default='', max_length=20)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('subtitle', models.CharField(blank=True, default='', max_length=512)),
                ('snippet', models.TextField(blank=True, default='')),
                ('published', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.author')),
            ],
        ),
    ]
