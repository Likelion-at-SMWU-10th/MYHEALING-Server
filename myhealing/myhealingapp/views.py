from django.shortcuts import render

def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'myhealingapp/index.html', _context)