from django.shortcuts import render
from tests_app.models import Test

# Create your views here.
def tests_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/tests_list.html', {'tests' : tests})

def about(request):
    return render(request, 'tests/about.html')

def test_detail(request, test_id):
    test = Test.objects.get(id=test_id)
    return render(request, 'tests/test_detail.html', {'test' : test})