from django.shortcuts import render, get_object_or_404, redirect
from tests_app.models import Test
from tests_app.forms import test

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
    return redirect("admin")

def test_create(request):
    if request.method == "POST":
        form = test.TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tests/admin/')
        else:
            return render(request, 'tests/create.html', {'form': form})
    
    # GET
    form = test.TestForm()
    return render(request, 'tests/create.html', {'form': form})

def test_edit(request, test_id):
    item = get_object_or_404(Test, id=test_id)
    
    if request.method == "POST":
        form = test.TestForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/tests/admin/')
        else:
            return render(request, 'tests/edit.html', {'form': form})
    
    # GET
    form = test.TestForm(instance=item)
    return render(request, 'tests/edit.html', {'form': form})
        
        