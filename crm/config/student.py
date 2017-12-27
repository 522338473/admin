import json
from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect

from stark.service import v1
from crm import models


class StudentConfig(v1.StarkConfig):


    list_display = ["id","username","emergency_contract","company",]

    show_search_form = True



v1.site.register(models.Student,StudentConfig)



