# Generated by Django 4.1 on 2022-08-18 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daily_words', '0002_word_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.IntegerField()),
                ('user_email', models.EmailField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='word',
            name='user_id',
        ),
        migrations.AddField(
            model_name='word',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words', to='daily_words.user'),
        ),
    ]
