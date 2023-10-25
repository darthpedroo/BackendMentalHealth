from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from django.db.models import Count
from base.models import Item, BlogPost
from .serializers import ItemSerializer, BlogSerializer, PhraseSerializer
from rest_framework import status
from rest_framework.views import APIView
from .utils import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
import base64
import os
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['pk'] = user.pk
        return token

class MyTokenOBtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser])
def getUserDetails(request):
    details = UserDetails.objects.all()  
    serializer = UserDetailsSerializer(details, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser])
def getSingleUserDetails(request , pk):
    details = UserDetails.objects.get(idUser = pk)
    serializer = UserDetailsSerializer(details, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserBio(request,pk):
    bio = UserBio.objects.get(idUser = pk)
    serializers = UserBioSerializer(bio, many = False)
    return Response(serializers.data)

@api_view(['POST'])
def addUserBio(request):
    serializer = UserBioSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def modifyUserBio(request,pk):
    data = request.data
    userBioInstance = UserBio.objects.get(idUser = pk)
    serializer = UserBioSerializer(instance=userBioInstance, data =data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def modifyUserDetails(request, pk):
    data = request.data
    userDetailsInstance = UserDetails.objects.get(idUser=pk)

    picturePath = userDetailsInstance.picture.path
    bannerPath = userDetailsInstance.banner.path

    with open(picturePath, 'rb') as image_file:
        image_binary = image_file.read()
        base64_encoded = base64.b64encode(image_binary)
        prev_picture = base64_encoded.decode('utf-8')
    
    with open(bannerPath, 'rb') as image_file:
        image_binary = image_file.read()
        base64_encoded = base64.b64encode(image_binary)
        prev_banner = base64_encoded.decode('utf-8')
    
    currentBanner = prev_banner
    currentPicture = prev_picture

    try:
        currentBanner = data['banner']
    except:
        currentPicture = data['picture']
    
    if currentPicture != prev_picture:
        os.remove(userDetailsInstance.picture.path)
    
    if currentBanner != prev_banner:
        os.remove(userDetailsInstance.banner.path)


    serializer = UserDetailsSerializer(instance=userDetailsInstance , data = data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addUserDetails(request):
    serializer = UserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getBlogPostsLIFO(request):
    notes = BlogPost.objects.all()
    serializer = BlogSerializer(notes, many= True)
    return Response(serializer.data)

@api_view(["GET"])
def getBlogPostsFIFO(request):
    notes = BlogPost.objects.all().order_by('-publishedDate')
    serializer = BlogSerializer(notes, many= True)
    return Response(serializer.data)

@api_view(["POST"])
def addBlogPost(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def addComment(request):
    serializer = CommentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"]) #Esto filtra un post segun el primary key
def getSinglePost(request,pk):
    post = BlogPost.objects.get(id=pk)
    serializer = BlogSerializer(post, many= False)
    return Response(serializer.data)

@api_view(['GET'])
def getAllUsers(request):
    users = User.objects.all()
    serializer =UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserByPk(request,pk):
    users = User.objects.get(id=pk)
    serializer =UserSerializer(users, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserByName(request,name):
    users = User.objects.get(username=name)
    serializer =UserSerializer(users, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def getAllComments(request):
    comments = Comments.objects.all()
    serializer = CommentsSerializer(comments, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getCommentByPostPk(request,pk):
    comments = Comments.objects.filter(postId=pk)
    serializer =CommentsSerializer(comments, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserPosts(request,pk):
    posts = BlogPost.objects.filter(idUser=pk)
    serializer = BlogSerializer(posts, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getNumOfUserPosts(requset,pk):
    postsCounter = BlogPost.objects.filter(idUser=pk).count()
    return Response(postsCounter)

@api_view(['GET'])
def getNumOfUserLikes(request,pk):
    likesCounter = Likes.objects.filter(idUser=pk, isDeleted =False).count()
    return Response(likesCounter)
    
@api_view(['GET'])
def getNumOfComments(request,pk):
    commentsCounter = Comments.objects.filter(authorId = pk).count()
    return Response(commentsCounter)

@api_view(['GET'])
def getLikesFromPosts(request):
    likesCounter = Likes.objects.filter(isDeleted = False)
    annotated_likesCounter = likesCounter.values('idPost').annotate(amountOfLikes=Count('id'))
    result = list(annotated_likesCounter)
    return Response(result)

@api_view(['GET'])
def getCommentsFromPosts(request):
    commentsCounter = Comments.objects.all()
    annotated_likesCounter = commentsCounter.values('postId').annotate(amountOfComments=Count('id'))
    result = list(annotated_likesCounter)
    return Response(result)


@api_view(['GET'])
def getLikes(request):
    likes = Likes.objects.all()
    serializers = LikesSerializer(likes , many = True)
    return Response(serializers.data)

@api_view(['GET','PUT'])
def getLikesByPost(request,pk):
    likes = Likes.objects.filter(idPost = pk)
    serializer = LikesSerializer(likes, many =True)
    return Response(serializer.data)

@api_view(['GET'])
def checkLikeExists(request,pk1,pk2): #1 = post 2 = user
    likes = Likes.objects.filter(idPost = pk1, idUser = pk2)
    if likes.exists():
        serializer = LikesSerializer(likes, many = True)
        return Response(serializer.data)
    else:
        return Response("Error")

@api_view(['GET'])
def getLikesByUser(request,pk):
    likes = Likes.objects.filter(idUser = pk)
    serializer = LikesSerializer(likes, many =True)
    return Response(serializer.data)

@api_view(['PUT'])
def softDeleteLike(request,pk):
    data = request.data
    like = Likes.objects.get(id = pk)
    serializer = LikesSerializer(instance=like ,data = data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
def addLike(request):
    serializer = LikesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def UserCreateView(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAvailablePhrases(request,phraseid):
    try:
        phrase = Phrase.objects.get(id=phraseid)
        serializer = PhraseSerializer(phrase)
        return Response(serializer.data)

    except Phrase.DoesNotExist:
        return Response({'message': 'No valid phrase found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getAllPhrases(request):
    phrases = Phrase.objects.all()
    serializer = PhraseSerializer(phrases, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def CreatePhrase(request):
    serializer = PhraseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createChatbotEntry(request):
    serializer = ChatBotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listChatbotEntries(request):
    entries = ChatBot.objects.all()
    serializer = ChatBotSerializer(entries, many=True)
    return Response(serializer.data)

@api_view(["GET"]) 
def getChatbotEntries(request,alocation):
    ChatBotEntry = ChatBot.objects.filter(location=alocation)
    serializer = ChatBotSerializer(ChatBotEntry, many= True)
    return Response(serializer.data)