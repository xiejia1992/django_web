# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Group(models.Model):
    '''  定义分组模型 '''
    group_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.group_name

class IP(models.Model):
    '''  定义IP地址模型 '''
    ip_address = models.CharField(max_length=128)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.ip_address
