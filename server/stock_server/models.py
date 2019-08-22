# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class A000100(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a000100'


class A000640(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a000640'


class A001630(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a001630'


class A006280(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a006280'


class A008930(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a008930'


class A009290(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a009290'


class A069620(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a069620'


class A096760(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a096760'


class A128940(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a128940'


class A249420(models.Model):
    stock_index = models.BigIntegerField(primary_key=True)
    stock_date = models.BigIntegerField(blank=True, null=True)
    stock_time = models.BigIntegerField(blank=True, null=True)
    stock_price = models.BigIntegerField(blank=True, null=True)
    stock_volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a249420'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
