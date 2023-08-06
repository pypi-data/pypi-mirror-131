from django import template
from krx_hj3415 import krx
from ..models import ModelFavStock

register = template.Library()

# takes_context로 부모 context를 이용하는 이유는 이전 페이지로 돌아가기 위해 페이지경로를 보내주기 위해서임.


@register.inclusion_tag('fav_stock/add_n_edit_fav.html', takes_context=True)
def add_n_edit_fav(context, code):
    try:
        # DB에 있으면 edit 모드
        o = ModelFavStock.objects.get(code=code)
        context.update({
            'mode': 'edit',
            'code': code,
            'name': o.name,
            'remarks': o.remarks
        })

    except ModelFavStock.DoesNotExist:
        # DB에 없으면 add 모드
        context.update({
            'mode': 'add',
            'code': code,
            'name': krx.get_name(code),
            'remarks': '',
        })
    return context


@register.inclusion_tag('fav_stock/del_fav.html', takes_context=True)
def del_fav(context, code):
    try:
        o = ModelFavStock.objects.get(code=code)
        context.update({
            'mode': 'del',
            'code': code,
            'is_exist': True,
        })

    except ModelFavStock.DoesNotExist:
        context.update({
            'mode': 'del',
            'code': code,
            'is_exist': False,
        })
    return context
