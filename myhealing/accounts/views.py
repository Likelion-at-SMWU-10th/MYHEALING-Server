from django.shortcuts import render
from django.shortcuts import redirect
import requests, json

def kakaoLoginLogic(request):
    _restApiKey = '0f35fc2805b692fffd8d94ff011d731a'
    _redirectUrl = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code'] # 인증 코드 가져오기
    _restApiKey = '0f35fc2805b692fffd8d94ff011d731a'
    _redirect_uri = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    _access_token = _result['access_token']

    # 사용자 정보 받아오기
    kakaoGetUserInfo(_access_token)

    request.session['access_token'] = _access_token
    request.session.modified = True
    return render(request, 'accounts/loginSuccess.html')

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
        return render(request, 'accounts/logoutSuccess.html')
    else:
        return render(request, 'accounts/logoutError.html')

def kakaoGetUserInfo(access_token):
    _user_info_json = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    _user_info_result = _user_info_json.json()
    _id_token = _user_info_result['id']
    _nickname = _user_info_result['kakao_account']['profile']['nickname']
    if 'profile_image_url' in  _user_info_result['kakao_account']['profile']:
        _photo_url =  _user_info_result['kakao_account']['profile']['profile_image_url']
    else:
        _photo_url = None
    
    if 'email' in _user_info_result['kakao_account']:
        _email =  _user_info_result['kakao_account']['email']
    else:
        _email = None
    
    # DB에 저장
    # 1) DB에 같은 id_token이 이미 존재하는 경우 > 로그인 & JWT 토큰 발행


    # 2) DB에 같은 id_token이 없는 경우 > 회원 가입 & JWT 토큰 발행