from django.db import models

# Create your models here.
class Role(models.Model):
    caption = models.CharField(max_length=16,verbose_name="角色名称",null=True,blank=True)
    class Meta:
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.caption

class UserType(models.Model):
    title = models.CharField(max_length=16,verbose_name="类型名称",null=True,blank=True)
    roles = models.ManyToManyField(to="Role")
    class Meta:
        verbose_name_plural = "用户类型表"
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=16,verbose_name="用户名",null=True,blank=True)
    email = models.EmailField(max_length=16,verbose_name="邮箱",null=True,blank=True)
    ut = models.ForeignKey(to="UserType",null=True,blank=True)
    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.name




class Iport(models.Model):
    hostname = models.CharField(max_length=32,verbose_name="主机名",null=True,blank=True)
    ip = models.GenericIPAddressField(protocol="ipv4",verbose_name="IP地址",null=True,blank=True)
    port = models.IntegerField(verbose_name="端口",null=True,blank=True)
    creat_time = models.TextField(verbose_name="备注信息",null=True,blank=True)