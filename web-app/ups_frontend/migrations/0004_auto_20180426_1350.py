# Generated by Django 2.0.4 on 2018-04-26 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ups_frontend', '0003_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ups_account', models.CharField(max_length=50)),
                ('amazon_account', models.CharField(max_length=50)),
                ('pos_x', models.CharField(max_length=30)),
                ('pos_y', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='curr_world',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='curr_world', max_length=30, null=True)),
                ('worldid', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tracking_number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worldid', models.CharField(max_length=30, null=True)),
                ('tracking_number', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worldid', models.CharField(default='', max_length=30, null=True)),
                ('truckid', models.CharField(max_length=30)),
                ('package_num', models.CharField(default='0', max_length=10)),
                ('status', models.CharField(choices=[('I', 'idel'), ('E', 'truck en route to warehouse'), ('W', 'truck waiting for package'), ('L', 'loaded and waiting for delivery'), ('O', 'out for delivery')], max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='time',
            name='O_time',
        ),
        migrations.AddField(
            model_name='item',
            name='worldid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='packageid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='truckid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='worldid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='packageid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='worldid',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('C', 'Created'), ('E', 'truck en route to warehouse'), ('W', 'truck waiting for package'), ('L', 'loaded and waiting for delivery'), ('O', 'out for delivery'), ('D', 'delivered')], max_length=30),
        ),
    ]
