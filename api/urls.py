from django.urls import path 
from . import views
from .views import MyTokenOBtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    #Blog Post
    path('add/',views.addBlogPost),
    path('postsLIFO/',views.getBlogPostsLIFO),
    path('postsFIFO/', views.getBlogPostsFIFO),
    path('posts/<str:pk>/',views.getSinglePost),
        
    #Comments
    path('add/comment',views.addComment),
    path('comments/',views.getAllComments),
    path('comments/<str:pk>',views.getCommentByPostPk),
    path('comments/<str:pk>/counter', views.getNumOfComments),
    path('commentsCounter/',views.getCommentsFromPosts),

    #Users
    path('users/',views.getAllUsers),
    path('users/<str:pk>/',views.getUserByPk),
    path('user/<str:name>/',views.getUserByName),
    path('users/<str:pk>/posts',views.getUserPosts),
    path('users/<str:pk>/postsCounter', views.getNumOfUserPosts),

    #Likes
    path('likes/',views.getLikes),
    path('add/like',views.addLike),
    path('likes/post/<str:pk>', views.getLikesByPost),
    path('likes/user/<str:pk>', views.getLikesByUser),
    path('likes/user/<str:pk>/counter',views.getNumOfUserLikes),
    path('likes/delete/<str:pk>',views.softDeleteLike),
    path('likes/<str:pk1>/<str:pk2>/', views.checkLikeExists),
    path('likes/counter/',views.getLikesFromPosts),

    #BIO

    path('bio/<str:pk>', views.getUserBio),
    path('addbio/',views.addUserBio),
    path('modifybio/<str:pk>',views.modifyUserBio ),
    
    #Jwt
    path('token/', MyTokenOBtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/',views.UserCreateView),
    
    #Images 
    path('images/', views.getUserDetails),
    path('images/<str:pk>/', views.getSingleUserDetails),
    path('add/images/', views.addUserDetails),
    path('modify/images/<str:pk>/', views.modifyUserDetails),

    #Frases
    path('valid-phrase/<int:phraseid>', views.getAvailablePhrases, name='get-available-phrase'),
    path('all-phrase/', views.getAllPhrases, name='get-all-phrases'),
    path('create-phrase/', views.CreatePhrase, name= 'crear-frase'),

    #Chatbot
    path('create_chatbot_entry/',  views.createChatbotEntry, name='create_chatbot_entry'),
    path('list_chatbot_entries/', views.listChatbotEntries, name='list_chatbot_entries'),
    path('chatbot_entry/<str:alocation>/',views.getChatbotEntries),
]