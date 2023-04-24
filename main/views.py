from django.shortcuts import render
#from django.http import HttpResponse
# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    data = {'title': "Главная страница",
            'values': ['some', 'hello', 123],
            'obj': {'car': 'BMW', 'age': 42, 'hobby': 'football'},
            'num_visits': num_visits}
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')