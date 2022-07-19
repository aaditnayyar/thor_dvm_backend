from django.shortcuts import render
from django.views import View
from datetime import datetime
#from urllib import urlencode
from django.conf import settings
from django.contrib import messages
#from app.models import User

# def google_login(request):
#     redirect_uri = "%s://%s%s" % (
#         request.scheme, request.get_host(), reverse('pain:google_login')
#     )
#     if('code' in request.GET):
#         params = {
#             'grant_type': 'authorization_code',
#             'code': request.GET.get('code'),
#             'redirect_uri': redirect_uri,
#             'client_id': settings.GP_CLIENT_ID,
#             'client_secret': settings.GP_CLIENT_SECRET
#         }
#         url = 'https://accounts.google.com/o/oauth2/token'
#         response = requests.post(url, data=params)
#         url = 'https://www.googleapis.com/oauth2/v1/userinfo'
#         access_token = response.json().get('access_token')
#         response = requests.get(url, params={'access_token': access_token})
#         user_data = response.json()
#         email = user_data.get('email')
#         if email:
#             user, _ = User.objects.get_or_create(email=email, username=email)
#             # gender = user_data.get('gender', '').lower()
#             # if gender == 'male':
#             #     gender = 'M'
#             # elif gender == 'female':
#             #     gender = 'F'
#             # else:
#             #     gender = 'O'
#             data = {
#                 'first_name': user_data.get('name', '').split()[0],
#                 #'last_name': user_data.get('family_name'),
#                 'google_avatar': user_data.get('picture'),
#                 #'gender': gender,
#                 'is_active': True
#             }
#             user.__dict__.update(data)
#             user.save()
#             user.backend = settings.AUTHENTICATION_BACKENDS[0]
#             login(request, user)
#         else:
#             messages.error(
#                 request,
#                 'Unable to login with Gmail Please try again'
#             )
#         return redirect('/')
#     else:
#         url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
#         scope = [
#             "https://www.googleapis.com/auth/userinfo.profile",
#             "https://www.googleapis.com/auth/userinfo.email"
#         ]
#         scope = " ".join(scope)
#         url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
#         return redirect(url)
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/index.html')