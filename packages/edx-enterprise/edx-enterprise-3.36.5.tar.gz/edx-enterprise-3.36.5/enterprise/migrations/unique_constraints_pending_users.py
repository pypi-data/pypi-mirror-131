# Generated by Django 2.2.17 on 2020-12-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0117_auto_20201215_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpendingenterprisecustomeruser',
            name='user_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='pendingenterprisecustomeruser',
            name='user_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterUniqueTogether(
            name='pendingenterprisecustomeradminuser',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='pendingenterprisecustomeradminuser',
            index=models.Index(fields=['user_email', 'enterprise_customer'], name='enterprise__user_em_fead22_idx'),
        ),
        migrations.AddIndex(
            model_name='pendingenterprisecustomeradminuser',
            index=models.Index(fields=['user_email'], name='enterprise__user_em_6e1f5b_idx'),
        ),
        migrations.AddIndex(
            model_name='pendingenterprisecustomeruser',
            index=models.Index(fields=['user_email', 'enterprise_customer'], name='enterprise__user_em_f98d36_idx'),
        ),
        migrations.AddIndex(
            model_name='pendingenterprisecustomeruser',
            index=models.Index(fields=['user_email'], name='enterprise__user_em_488930_idx'),
        ),
        migrations.AddConstraint(
            model_name='pendingenterprisecustomeradminuser',
            constraint=models.UniqueConstraint(fields=('user_email', 'enterprise_customer'), name='unique pending admin user and EnterpriseCustomer'),
        ),
        migrations.AddConstraint(
            model_name='pendingenterprisecustomeruser',
            constraint=models.UniqueConstraint(fields=('user_email', 'enterprise_customer'), name='unique user and EnterpriseCustomer'),
        ),
    ]
