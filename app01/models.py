from django.db import models

# Create your models here.
class Role(models.Model):
    caption = models.CharField(max_length=16,verbose_name="角色名称")
    class Meta:
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.caption

class UserType(models.Model):
    title = models.CharField(max_length=16,verbose_name="类型名称")
    roles = models.ManyToManyField(to="Role")
    class Meta:
        verbose_name_plural = "用户类型表"
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=16,verbose_name="用户名")
    email = models.EmailField(max_length=16,verbose_name="邮箱")
    ut = models.ForeignKey(to="UserType")
    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.name







# class UserInfo(models.Model):
#     name = models.CharField(max_length=32)
#
#
# class Role(models.Model):
#     name = models.CharField(max_length=32)
#
#
#
# class UserType(models.Model):
#     title = models.CharField(max_length=32)