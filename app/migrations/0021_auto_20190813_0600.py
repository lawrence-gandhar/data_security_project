# Generated by Django 2.2.3 on 2019-08-13 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20190813_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordsmanagement',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Brand'),
        ),
        migrations.AlterField(
            model_name='recordsmanagement',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='record_category', to='app.Category'),
        ),
        migrations.AlterField(
            model_name='recordsmanagement',
            name='record_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.FileSubmission'),
        ),
        migrations.AlterField(
            model_name='recordsmanagement',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='record_sub_category', to='app.Category'),
        ),
    ]