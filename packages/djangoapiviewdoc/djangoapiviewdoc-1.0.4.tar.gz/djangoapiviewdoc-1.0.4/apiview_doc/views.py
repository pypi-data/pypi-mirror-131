#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/12/14 13:26
    Desc  :
--------------------------------------
"""
from django.shortcuts import render

from apiview_doc.decorator import api_doc


def docs(request):
    context = api_doc()

    return render(request, 'apiview_doc/docs/index.html', context)
