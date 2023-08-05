from django.shortcuts import render, get_object_or_404
from .models import Cases, Category

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


def test_details(request, id: int):
    context = _make_case_details_context(id, 'cases/skel.html')
    logger.info(context)
    return render(request, 'cases/test_details.html', context)


def case_details_lightbox(request, id: int, skel_path: str):
    context = _make_case_details_context(id, skel_path)
    logger.info(context)
    return render(request, 'cases/case_details_lightbox.html', context)


def case_details_newpage(request, id: int, skel_path: str):
    context = _make_case_details_context(id, skel_path)
    logger.info(context)
    return render(request, 'cases/case_details_newpage.html', context)


def make_cases_context() -> dict:
    context = {
        'cases': {
            'p': '주목할 만한 치과 케이스 모음',
            'categories': Category.objects,
            'items': Cases.objects
        }
    }
    return context


def _make_case_details_context(id: int, skel_path: str) -> dict:
    context = {
        'skel_path': skel_path,
        'obj': get_object_or_404(Cases, pk=id),
    }
    return context

