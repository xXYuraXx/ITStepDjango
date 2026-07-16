from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

from tests_app import test_repo
from tests_app.forms import test_form
from tests_app.models import Option, Question, Test


def _can_manage_test(user, test_item):
    return user.is_staff or (user.is_authenticated and test_item.author_id == user.id)


def _manage_test_required(view):
    return login_required(view)


def _staff_required(view):
    return user_passes_test(lambda user: user.is_staff)(view)


def _get_test_form_class(user):
    return test_form.TestStaffForm if user.is_staff else test_form.TestBaseForm


def _blank_option(index):
    return {
        "index": index,
        "text": "",
        "is_correct": False,
        "match_text": "",
    }


def _blank_question_block(index):
    return {
        "index": index,
        "question_type": "single_select",
        "question_text": "",
        "correct_val": 1,
        "correct_text": "",
        "options": [_blank_option(0), _blank_option(1)],
    }


def _question_to_block(question, index):
    options = [
        {
            "index": option_index,
            "text": option.text,
            "is_correct": option.is_correct,
            "match_text": option.match_text,
        }
        for option_index, option in enumerate(question.options.all())
    ]
    if not options:
        options = [_blank_option(0), _blank_option(1)]

    return {
        "index": index,
        "question_type": question.question_type,
        "question_text": question.question_text,
        "correct_val": question.correct_val,
        "correct_text": question.correct_text,
        "options": options,
    }


def _build_question_blocks(test_item=None):
    if test_item is None:
        return [_blank_question_block(0)]

    blocks = []
    for index, question in enumerate(test_item.questions.order_by("order").prefetch_related("options")):
        blocks.append(_question_to_block(question, index))

    return blocks or [_blank_question_block(0)]


def _build_question_blocks_from_post(post_data):
    question_blocks = []
    question_index = 0

    while True:
        question_text_key = f"question_{question_index}_question_text"
        if question_text_key not in post_data:
            break

        option_payloads = []
        option_index = 0
        while True:
            option_text_key = f"question_{question_index}_option_{option_index}_text"
            option_match_key = f"question_{question_index}_option_{option_index}_match_text"
            option_correct_key = f"question_{question_index}_option_{option_index}_is_correct"

            if option_text_key not in post_data and option_match_key not in post_data and option_correct_key not in post_data:
                break

            option_payloads.append(
                {
                    "index": option_index,
                    "text": post_data.get(option_text_key, ""),
                    "is_correct": option_correct_key in post_data,
                    "match_text": post_data.get(option_match_key, ""),
                }
            )
            option_index += 1

        if not option_payloads:
            option_payloads = [_blank_option(0), _blank_option(1)]

        question_blocks.append(
            {
                "index": question_index,
                "question_type": post_data.get(f"question_{question_index}_question_type", "single_select"),
                "question_text": post_data.get(question_text_key, ""),
                "correct_val": post_data.get(f"question_{question_index}_correct_val", "1"),
                "correct_text": post_data.get(f"question_{question_index}_correct_text", ""),
                "options": option_payloads,
            }
        )
        question_index += 1

    return question_blocks or [_blank_question_block(0)]


def _normalize_text(value):
    return (value or "").strip().casefold()


def _extract_question_payloads(post_data):
    payloads = []
    question_index = 0

    while True:
        question_text_key = f"question_{question_index}_question_text"
        if question_text_key not in post_data:
            break

        question_text = post_data.get(question_text_key, "").strip()
        question_type = post_data.get(f"question_{question_index}_question_type", "single_select")
        correct_val = post_data.get(f"question_{question_index}_correct_val", "1")
        correct_text = post_data.get(f"question_{question_index}_correct_text", "").strip()

        option_payloads = []
        option_index = 0
        while True:
            option_text_key = f"question_{question_index}_option_{option_index}_text"
            option_match_key = f"question_{question_index}_option_{option_index}_match_text"
            option_correct_key = f"question_{question_index}_option_{option_index}_is_correct"

            if option_text_key not in post_data and option_match_key not in post_data and option_correct_key not in post_data:
                break

            option_text = post_data.get(option_text_key, "").strip()
            option_match_text = post_data.get(option_match_key, "").strip()
            option_is_correct = option_correct_key in post_data

            if option_text or option_match_text or option_is_correct:
                option_payloads.append(
                    {
                        "text": option_text,
                        "match_text": option_match_text,
                        "is_correct": option_is_correct,
                    }
                )

            option_index += 1

        if question_text or correct_text or option_payloads:
            payloads.append(
                {
                    "question_type": question_type,
                    "question_text": question_text,
                    "correct_val": correct_val,
                    "correct_text": correct_text,
                    "options": option_payloads,
                }
            )

        question_index += 1

    return payloads


def _save_question_payloads(test_item, payloads):
    test_item.questions.all().delete()

    for order, payload in enumerate(payloads, start=1):
        question = Question.objects.create(
            test=test_item,
            question_type=payload["question_type"],
            question_text=payload["question_text"],
            correct_val=payload["correct_val"] or 0,
            correct_text=payload["correct_text"],
            order=order,
        )

        for option_payload in payload["options"]:
            if not option_payload["text"] and not option_payload["match_text"]:
                continue

            Option.objects.create(
                question=question,
                text=option_payload["text"],
                match_text=option_payload["match_text"],
                is_correct=option_payload["is_correct"],
            )


def _reset_progress(request, test_item):
    questions = list(test_item.questions.order_by("order").prefetch_related("options"))
    progress = {
        "test_id": test_item.id,
        "question_ids": [question.id for question in questions],
        "current_index": 0,
        "answers": {},
        "finished": False,
    }
    test_repo.set_progress(request, test_item.id, progress)
    test_repo.set_score(request, test_item.id, 0)
    return progress


def _get_progress_or_reset(request, test_item):
    progress = test_repo.get_progress(request, test_item.id)
    questions = list(test_item.questions.order_by("order").prefetch_related("options"))
    question_ids = [question.id for question in questions]

    if not progress or progress.get("question_ids") != question_ids:
        progress = _reset_progress(request, test_item)

    return progress, questions


def _get_current_question(progress, questions):
    current_index = progress.get("current_index", 0)
    if current_index < 0 or current_index >= len(questions):
        return None
    return questions[current_index]


def _grade_question(question, post_data):
    if question.question_type == "single_select":
        selected_option_id = post_data.get("selected_option")
        selected_option = question.options.filter(id=selected_option_id).first()
        return bool(selected_option and selected_option.is_correct)

    if question.question_type == "multi_select":
        selected_ids = {str(option_id) for option_id in post_data.getlist("selected_options")}
        correct_ids = {str(option_id) for option_id in question.options.filter(is_correct=True).values_list("id", flat=True)}
        return selected_ids == correct_ids

    if question.question_type == "text_input":
        submitted_text = _normalize_text(post_data.get("text_answer"))
        return submitted_text == _normalize_text(question.correct_text)

    if question.question_type == "matching":
        for option in question.options.all():
            submitted_match = post_data.get(f"match_{option.id}", "")
            if _normalize_text(submitted_match) != _normalize_text(option.match_text):
                return False
        return True

    return False


def _build_question_context(question):
    options = list(question.options.all())
    match_choices = []

    if question.question_type == "matching":
        match_choices = [option.match_text for option in options if option.match_text]

    return {
        "question": question,
        "options": options,
        "match_choices": match_choices,
    }


def tests_list(request):
    tests = Test.objects.select_related("author", "genre").all()
    favorite_ids = set(test_repo.get_favorite_ids(request))
    return render(
        request,
        'tests/tests_list.html',
        {'tests': tests, 'favorite_ids': favorite_ids},
    )


def about(request):
    return render(request, 'tests/about.html')


def test_detail(request, test_id):
    test_item = get_object_or_404(Test.objects.select_related("author", "genre"), id=test_id)
    test_item.count_views += 1
    test_item.save(update_fields=["count_views"])
    is_favorite = test_repo.is_favorite(request, test_item.id)
    return render(
        request,
        'tests/test_detail.html',
        {
            'test': test_item,
            'is_favorite': is_favorite,
            'can_edit': _can_manage_test(request.user, test_item),
        },
    )


@_staff_required
def admin_list(request):
    tests = Test.objects.select_related("author", "genre").all()
    return render(request, 'tests/admin.html', {'tests': tests})


@login_required
def test_delete(request, test_id):
    test_item = get_object_or_404(Test, id=test_id)

    if not _can_manage_test(request.user, test_item):
        raise PermissionDenied

    test_item.delete()
    messages.success(request, 'Test deleted successfully!')
    return redirect("admin" if request.user.is_staff else "tests_list")


@login_required
def test_create(request):
    form_class = _get_test_form_class(request.user)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        question_payloads = _extract_question_payloads(request.POST)
        question_blocks = _build_question_blocks_from_post(request.POST)

        if form.is_valid() and question_payloads:
            with transaction.atomic():
                test_item = form.save(commit=False)
                if not request.user.is_staff:
                    test_item.author = request.user
                test_item.save()
                _save_question_payloads(test_item, question_payloads)

            messages.success(request, 'Test created successfully!')
            if request.user.is_staff:
                return redirect('admin')
            return redirect('test_detail', test_id=test_item.id)

        messages.error(request, 'Please fill in the test details and add at least one question.')
    else:
        form = form_class()
        question_blocks = _build_question_blocks()

    return render(
        request,
        'tests/create.html',
        {
            'form': form,
            'question_blocks': question_blocks,
            'question_types': Question.QUESTION_TYPES,
            'can_assign_author': request.user.is_staff,
        },
    )


@login_required
def test_edit(request, test_id, return_url=None):
    test_item = get_object_or_404(Test, id=test_id)

    if not _can_manage_test(request.user, test_item):
        raise PermissionDenied

    form_class = _get_test_form_class(request.user)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=test_item)
        question_payloads = _extract_question_payloads(request.POST)
        question_blocks = _build_question_blocks_from_post(request.POST)

        if form.is_valid() and question_payloads:
            with transaction.atomic():
                updated_test = form.save(commit=False)
                if not request.user.is_staff:
                    updated_test.author = request.user
                updated_test.save()
                _save_question_payloads(updated_test, question_payloads)

            messages.success(request, 'Test edited successfully!')
            if return_url:
                return redirect(return_url)
            if request.user.is_staff:
                return redirect('admin')
            return redirect('test_detail', test_id=test_item.id)

        messages.error(request, 'Please fix the form and keep at least one question.')
    else:
        form = form_class(instance=test_item)
        question_blocks = _build_question_blocks(test_item)

    return render(
        request,
        'tests/edit.html',
        {
            'form': form,
            'question_blocks': question_blocks,
            'question_types': Question.QUESTION_TYPES,
            'test': test_item,
            'can_assign_author': request.user.is_staff,
        },
    )


def search_by_id(request):
    return render(request, 'tests/search_by_id.html')


def test_start(request, test_id):
    test_item = get_object_or_404(Test.objects.select_related("author", "genre"), id=test_id)
    questions = list(test_item.questions.order_by("order").prefetch_related("options"))

    if not questions:
        messages.error(request, 'This test has no questions yet.')
        return redirect('test_detail', test_id=test_id)

    _reset_progress(request, test_item)
    return redirect('test_question', test_id=test_id, question_order=1)


def test_question(request, test_id, question_order):
    test_item = get_object_or_404(Test.objects.select_related("author", "genre"), id=test_id)
    progress, questions = _get_progress_or_reset(request, test_item)

    if question_order < 1:
        messages.error(request, 'Invalid question order.')
        return redirect('test_detail', test_id=test_id)

    current_question = _get_current_question(progress, questions)

    if current_question is None:
        return redirect('test_result', test_id=test_id)

    expected_order = current_question.order
    if question_order != expected_order:
        return redirect('test_question', test_id=test_id, question_order=expected_order)

    if request.method == "POST":
        is_correct = _grade_question(current_question, request.POST)
        answers = progress.get("answers", {})
        answers[str(current_question.id)] = {
            "question_text": current_question.question_text,
            "is_correct": is_correct,
            "question_type": current_question.question_type,
        }
        progress["answers"] = answers
        progress["current_index"] = progress.get("current_index", 0) + 1

        if is_correct:
            test_repo.add_score(request, test_id, value=current_question.correct_val)

        next_question = _get_current_question(progress, questions)
        progress["finished"] = next_question is None
        test_repo.set_progress(request, test_id, progress)

        if next_question is None:
            return redirect('test_result', test_id=test_id)

        return redirect('test_question', test_id=test_id, question_order=next_question.order)

    context = _build_question_context(current_question)
    context.update(
        {
            'test': test_item,
            'test_id': test_id,
            'question_order': question_order,
            'current_score': test_repo.get_score(request, test_id),
            'progress_total': len(questions),
        }
    )
    return render(request, 'tests/test_question.html', context)


def test_result(request, test_id):
    test_item = get_object_or_404(Test.objects.select_related("author", "genre"), id=test_id)
    progress = test_repo.get_progress(request, test_id)
    questions = list(test_item.questions.order_by("order").prefetch_related("options"))

    if not progress:
        return redirect('test_detail', test_id=test_id)

    if not progress.get("finished") and questions:
        current_index = progress.get("current_index", 0)
        if current_index < len(questions):
            return redirect('test_question', test_id=test_id, question_order=questions[current_index].order)

    total_points = sum(question.correct_val for question in questions)
    answers = progress.get("answers", {})
    answer_rows = [
        {
            "question": question,
            "answer": answers.get(str(question.id), {}),
        }
        for question in questions
    ]

    return render(
        request,
        'tests/result.html',
        {
            'test': test_item,
            'questions': questions,
            'answer_rows': answer_rows,
            'score': test_repo.get_score(request, test_id),
            'total_points': total_points,
        },
    )
