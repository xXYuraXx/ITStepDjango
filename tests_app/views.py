from django.shortcuts import render, get_object_or_404, redirect
from tests_app.models import Test

# Create your views here.
def tests_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/tests_list.html', {'tests' : tests})

def about(request):
    return render(request, 'tests/about.html')

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'tests/test_detail.html', {'test' : test})

def admin_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/admin.html', {'tests' : tests})

def test_delete(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    return redirect("admin")