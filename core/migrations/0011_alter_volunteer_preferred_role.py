# Generated by Django 3.2.14 on 2022-07-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20220601_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='preferred_role',
            field=models.CharField(choices=[('Teaching', 'TEACHING'), ('Teaching Assistant', 'TEACHING ASSISTANT'), ('Special Needs', 'SPECIAL NEEDS'), ('IT', 'IT')], max_length=18),
        ),
    ]
