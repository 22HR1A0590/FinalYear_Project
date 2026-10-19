from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('registration/',registration,name='registration'),
    path('login/', login , name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload/',upload , name='upload'),
    path('search/' , search , name='search'),
    path('request_file/<doc_id>/' , request_file , name='request_file'),
    path('view_request/' , view_request , name='view_request'),
    path('data_owner_dashboard/', data_owner_dashboard , name='data_owner_dashboard'),
    path('data_user_dashboard/' , data_user_dashboard, name='data_user_dashboard'),
    path('request/accept/<int:id>/', accept_req , name='accept_req'),
    path('request/reject/<int:id>/' , reject_req , name='reject_req'),
    path('view_file/' , view_file , name='view_file'),
    path('view_response/' , view_response , name='view_response'),
    path('view_requestfile/' , view_requestfile , name='view_requestfile'),
    path('download/<doc_id>' , download , name='download'),
    path('serverA_login/' , serverA_login , name='serverA_login'),
    path('serverA_dashboard/' , serverA_dashboard , name='serverA_dashboard'),
    path('serverB_dashboard/' , serverB_dashboard , name='serverB_dashboard'),
    path('serverC_dashboard/' , serverC_dashboard , name='serverC_dashboard'),
    path('serverA_files/' , serverA_files , name = 'serverA_files'),
    path('serverB_files/' , serverB_files , name='serverB_files'),
    path('serverC_files/' , serverC_files , name='serverC_files'),
    path('download/<doc_id>/' , download , name='download'),
    path('server_login/', server_login, name='server_login'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('view_profile/' , view_profile , name='view_profile'),
    path('update_profile/' , update_profile , name='update_profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
