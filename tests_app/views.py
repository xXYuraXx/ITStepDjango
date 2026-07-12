from django.shortcuts import render, get_object_or_404, redirect
from tests_app.models import Test, TestQuestion
from tests_app.forms import test_form
from django.contrib import messages
from tests_app import test_repo

# Create your views here.
def tests_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/tests_list.html', {'tests' : tests})

def about(request):
    return render(request, 'tests/about.html')

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.count_views += 1
    test.save()
    return render(request, 'tests/test_detail.html', {'test' : test})

def admin_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/admin.html', {'tests' : tests})

def test_delete(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    messages.success(request, 'Test deleted successfully!')
    return redirect("admin")

def test_create(request):
    if request.method == "POST":
        form = test_form.TestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Test created successfully!')
            return redirect('/tests/admin/')
        else:
            return render(request, 'tests/create.html', {'form': form})
    
    # GET
    form = test_form.TestForm()
    return render(request, 'tests/create.html', {'form': form})

def test_edit(request, test_id, return_url=None):
    item = get_object_or_404(Test, id=test_id)
    
    if request.method == "POST":
        form = test_form.TestForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Test edited successfully!')
            if return_url:
                return redirect(return_url)
            return redirect('/tests/admin/')
        else:
            return render(request, 'tests/edit.html', {'form': form})
    
    # GET
    form = test_form.TestForm(instance=item)
    return render(request, 'tests/edit.html', {'form': form})
        

def search_by_id(request):
    return render(request, 'tests/search_by_id.html')


def test_question(request, test_id, question_order):
    
    if question_order < 1:
        messages.error(request, 'Invalid question order.')
        return redirect('test_detail', test_id=test_id)
    
    if question_order == 1:
        test_repo.set_score(request, test_id, 0)
        
    test_item = get_object_or_404(Test, id=test_id)
    testQuestion = TestQuestion.objects.filter(test=test_item, order=question_order).first()
    is_question_exists = testQuestion is not None
    
    if is_question_exists == False:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request, 'You have completed the test, your score is: ' + str(test_repo.get_score(request, test_id)))
        return redirect('test_detail', test_id=test_id)
    
    question = testQuestion.question
    
    if request.method == "POST":
        if 'testQuestions' not in request.POST:
            messages.error(request, 'Please select an answer before submitting.')
            return redirect('test_question', test_id=test_id, question_order=question_order)
        
        selected_option_id = request.POST.get('testQuestions')
        selected_option = question.options.filter(id=selected_option_id).first()
        
        value = 0
        if selected_option:
            if selected_option.is_correct:
                messages.info(request, 'Correct!')
                value = question.correct_val
            else:
                messages.error(request, 'Incorrect.')
                pass
        
        test_repo.add_score(request, test_id, value=value)
        return redirect('test_question', test_id=test_id, question_order=question_order + 1)
    
    # GET
    options = question.options.all()
    
    return render(request, 'tests/test_question.html', {'test': test_item,
                                                        'question': question,
                                                        'options': options,
                                                        'test_id': test_id,
                                                        'question_order': question_order,
                                                        'current_score': test_repo.get_score(request, test_id)})