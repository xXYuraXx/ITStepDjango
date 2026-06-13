from django.shortcuts import render

tests = [
    {
        'id': 1,
        'name': 'Додавання і віднімання раціональних чисел ',
        'description': 'Математика 6 клас',
        'author' : 'Яремків О. В.',
        'image': 'https://www.englishdom.com/dynamicus/blog-post/000/002/256/1621948173_content_700x455.jpg',
    },
    {
        'id': 2,
        'name': 'Дієслово ',
        'description': 'Українська мова 4 клас',
        'author' : 'Некрашевич С. А.',
        'image': 'https://www.bsmu.edu.ua/wp-content/uploads/2023/10/003axj-dbc4.jpg',
    },
    {
        'id': 3,
        'name': '"Різдвяна пісня в прозі" ',
        'description': 'Зарубіжна література 6 клас',
        'author' : 'Бовда О. ',
        'image': 'https://naurok-test.nyc3.cdn.digitaloceanspaces.com/145717/images/502457_1557645597.jpg',
    },
]



# Create your views here.
def tests_list(request):
    return render(request, 'tests/tests_list.html', {'tests' : tests})

def about(request):
    return render(request, 'tests/about.html')

def test_detail(request, test_id):
    test = None
    for t in tests:
        if t['id'] == test_id:
            test = t
            break
        
    return render(request, 'tests/test_detail.html', {'test' : test})