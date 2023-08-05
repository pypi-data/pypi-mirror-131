from django.shortcuts import render, get_object_or_404
from .models import Cases, Category
import os

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def test(request):
    context = make_cases_context()
    return render(request, 'cases/test.html', context)


def case_details(request, id: int, app_name: str):
    context = {
        'skel_path': os.path.join(app_name, 'skel.html'),
        'obj': get_object_or_404(Cases, pk=id),
    }
    logger.info(context)
    return render(request, 'cases/case_details.html', context)


def make_cases_context() -> dict:
    context = {
        'cases': {
            'p': '주목할 만한 치과 케이스 모음',
            'categories': Category.objects,
            'items': Cases.objects
        }
    }
    return context
