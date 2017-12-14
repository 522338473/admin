from django.db import models

# Create your models here.
# class Role(models.Model):
#     caption = models.CharField(max_length=16)
#     class Meta:
#         verbose_name_plural = "角色表"
#     def __str__(self):
#         return self.caption
#
# class UserType(models.Model):
#     title = models.CharField(max_length=16)
#     roles = models.ManyToManyField(to="Role")
#     class Meta:
#         verbose_name_plural = "用户类型表"
#     def __str__(self):
#         return self.title
#
# class UserInfo(models.Model):
#     name = models.CharField(max_length=16)
#     email = models.EmailField(max_length=16)
#     ut = models.ForeignKey(to="UserType",null=True,blank=True)
#     class Meta:
#         verbose_name_plural = "用户表"
#     def __str__(self):
#         return self.name







class UserInfo(models.Model):
    name = models.CharField(max_length=32)


class Role(models.Model):
    name = models.CharField(max_length=32)



class UserType(models.Model):
    title = models.CharField(max_length=32)