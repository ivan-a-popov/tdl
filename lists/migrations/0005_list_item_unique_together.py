# Generated by Django 3.2.10 on 2022-05-04 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20211223_0842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]
