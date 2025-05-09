from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class User(Model):
    userid = fields.CharField(max_length=11, pk=True)
    company_name = fields.CharField(max_length=30)
    group_name = fields.CharField(max_length=30, null=True)
    is_admin = fields.BooleanField(default=False)
    uscid = fields.CharField(max_length=30)
    dsj_username = fields.CharField(max_length=30)
    dsj_password = fields.CharField(max_length=30)
    bank_name = fields.CharField(max_length=30)
    bank_id = fields.CharField(max_length=30)
    staff_record = fields.JSONField(null=True,default=list)
    is_zero = fields.BooleanField(default=False)
    is_bill = fields.BooleanField(default=False)
    puppet_id = fields.CharField(max_length=30, null=True)
    invoice_habit = fields.TextField(null=True)
    create_time = fields.DatetimeField(auto_now_add=True, null=True)
    update_time = fields.DatetimeField(auto_now=True, null=True)
    enable = fields.BooleanField(default=True)

    class Meta:
        table = "users"

class Task(Model):
    id = fields.IntField(pk=True, generated=True)
    type = fields.CharField(max_length=255)
    input = fields.JSONField()
    output = fields.JSONField(null=True)
    state = fields.CharField(max_length=10, default="waiting")
    message = fields.TextField(null=True)
    userid = fields.CharField(max_length=30, default="0")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"

class Log(Model):
    id = fields.IntField(pk=True, generated=True)
    type = fields.CharField(max_length=30)
    title = fields.CharField(max_length=255)
    state = fields.BooleanField(default=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "logs"

class Message(Model):
    id = fields.IntField(pk=True, generated=True)
    userid = fields.CharField(max_length=30)
    serviceid= fields.CharField(max_length=30)
    messages=fields.JSONField(default=list)
    answer=fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "messages"