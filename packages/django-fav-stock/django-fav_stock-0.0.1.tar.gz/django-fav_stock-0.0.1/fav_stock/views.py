import math
import datetime

from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from eval_hj3415 import eval as eval_pkg

from .models import ModelFavStock

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def test(request):
    return render(request, 'fav_stock/test.html', {})


def add_n_edit_fav(request):
    if request.method == 'POST':
        logger.info(f'request.POST : {request.POST}')
        m = ''
        if request.POST['mode'] == 'add':
            code = request.POST['code']
            name = request.POST['name']
            remarks = str(request.POST['remarks']) + f"({datetime.datetime.today().date().strftime('%Y.%m.%d')})"
            red_price = eval_pkg.red(code=code)['red_price']
            red = None if math.isnan(red_price) else red_price  # red_price가 nan의 경우 에러발생하여 None으로 바꿈

            o = ModelFavStock(code=code, name=name, remarks=remarks, red=red)
            o.save()
            m = f"{code} added in favorite db."
        elif request.POST['mode'] == 'edit':
            code = request.POST['code']
            name = request.POST['name']
            remarks = request.POST['remarks']
            red_price = eval_pkg.red(code=code)['red_price']
            red = None if math.isnan(red_price) else red_price  # red_price가 nan의 경우 에러발생하여 None으로 바꿈

            o = get_object_or_404(ModelFavStock, code__exact=code)
            o.red = red
            o.remarks = remarks
            o.save()
            m = f"{code} {name} was edited in favorite."

        messages.add_message(request, messages.SUCCESS, m)
        logger.info(f'message : {m}')

        # How to redirect previous page
        # https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330
        n = request.POST.get('next', '/')
        return HttpResponseRedirect(n)


def del_fav(request):
    if request.method == 'POST':
        logger.info(f'request.POST : {request.POST}')

        code = request.POST['code']
        o = get_object_or_404(ModelFavStock, code__exact=code)
        o.delete()

        m = f"{o.code} {o.name} was deleted in favorite."
        messages.add_message(request, messages.SUCCESS, m)
        logger.info(f'message : {m}')

        # How to redirect previous page
        # https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330
        n = request.POST.get('next', '/')
        return HttpResponseRedirect(n)
