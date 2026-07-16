from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from tests_app import test_repo
from tests_app.models import Test


def favorites_list(request):
    favorite_ids = [int(value) for value in test_repo.get_favorite_ids(request)]
    tests = Test.objects.select_related("author", "genre").filter(id__in=favorite_ids)
    tests_by_id = {test.id: test for test in tests}
    ordered_tests = [tests_by_id[test_id] for test_id in favorite_ids if test_id in tests_by_id]

    return render(
        request,
        "favorites/list.html",
        {
            "tests": ordered_tests,
        },
    )


def favorite_toggle(request, test_id):
    test_item = get_object_or_404(Test, id=test_id)
    is_favorite = test_repo.toggle_favorite(request, test_item.id)

    if is_favorite:
        messages.success(request, f'"{test_item.name}" was added to favorites.')
    else:
        messages.info(request, f'"{test_item.name}" was removed from favorites.')

    next_url = request.META.get("HTTP_REFERER") or reverse("favorites_list")
    return redirect(next_url)