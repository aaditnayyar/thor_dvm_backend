# Generated by Django 4.0.6 on 2022-07-09 11:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.post')),
            ],
        ),
    ]
