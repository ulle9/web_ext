from django.shortcuts import render
#from django.http import HttpResponse
# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    data = {'title': "Инструментарий для работы с концептуальными схемами в родоструктурной форме Web-exteor",
            'num_visits': num_visits}
    return render(request, 'main/index.html', data)

def directory(request):
    return render(request, 'main/directory.html')