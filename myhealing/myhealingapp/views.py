from django.shortcuts import render
from django.shortcuts import redirect
import requests

def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'myhealingapp/index.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '0f35fc2805b692fffd8d94ff011d731a'
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code'] # 인증 코드 가져오기
    _restApiKey = '0f35fc2805b692fffd8d94ff011d731a'
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'myhealingapp/loginSuccess.html')

def kakaoLogout(request):
    _token = request.session['access_token']
    # 토큰 만료
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
        'Authorization': f'bearer {_token}'
    }

    # 연결 끊기
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #     'Authorization': f'bearer {_token}'
    # }

    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'myhealingapp/logoutSuccess.html')
    else:
        return render(request, 'myhealingapp/logoutError.html')