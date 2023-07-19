from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .schema import schema
from .serializers import UserSerializer
from .models import User, Group



class UserRegistrationView(APIView):
    def post(self, request):  #, format=None
        serializer = UserSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserAuth():
    def authenticate(self, username=None, password=None): # 
        
        try:
            user = User.objects.get(username=username)            
        except User.DoesNotExist:
            return None
        if user.password == password:
            return user

class UserLoginView(APIView):
        
    def post(self, request):  #, *args, **kwargs
        username = request.data.get('username')
        password = request.data.get('password')        

        user = UserAuth.authenticate(self, username=username, password=password)

        if user is not None:            
            # login(request, user)
            return Response({'message' : 'login successful.'}, status=status.HTTP_200_OK )
        else:
            return Response({'message' : 'Invalid! credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# one to one message

class SendMessageAPIView(APIView):
    def post(self, request):
        sender_name = request.data.get('sender')
        receiver_name = request.data.get('receiver')
        content = request.data.get('content')
        
        query = '''
            mutation {
                createMessage(senderName: "%s", receiverName: "%s", content: "%s") {
                    success
                    message {
                        id
                        sender {
                            id
                            username
                        }
                        receiver {
                            id
                            username
                        }
                        content
                    }
                }
            }
        ''' % (sender_name, receiver_name, content)

        result = schema.execute(query)
        if result.errors:
            return Response({'errors': [str(error) for error in result.errors]}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result.data['createMessage'])
    

# group message
class SendGroupMessageAPIView(APIView):
    def post(self, request):        
        sender_name = request.data.get('sender')        
        group_name = request.data.get('group')
        content = request.data.get('content')
        
        query = '''
            mutation {
                createGroupmessage(senderName: "%s", groupName: "%s", content: "%s") {
                    success
                    message {
                        id
                        sender {
                            id
                            username
                        }
                        group {
                            id
                            name
                        }
                        content
                    }
                }
            }
        ''' % (sender_name, group_name, content)

        sender = User.objects.get(username = sender_name)
        group = Group.objects.get(name = group_name)            
        if sender in group.members.all():
            result = schema.execute(query)
            if result.errors:
                return Response({'errors': [str(error) for error in result.errors]}, status=status.HTTP_400_BAD_REQUEST)
            return Response(result.data['createGroupmessage'])
        else:
            return Response({'error': 'Only group members can send messages to the group.'}, status=status.HTTP_403_FORBIDDEN)
        

# user received messages
class UserReceivedMessagesAPIView(APIView):
    def get(self, request, sender, receiver):
        query = '''
            query {
                userReceivedmessages(sender: "%s", receiver: "%s") {                                                        
                    content
                }
            }
        ''' % (sender, receiver)
        
        result = schema.execute(query)        
        if result.errors:            
            return Response({'errors': [str(error) for error in result.errors]}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result.data['userReceivedmessages'])



# user received group message
class UserReceivedGroupMessagesAPIView(APIView):
    def get(self, request, receiver, groupname):
        query = '''
            query {
                userReceivedgroupmessages(groupName: "%s") {                                        
                    sender {                        
                        username
                    }                    
                    content
                }
            }
        ''' % groupname

        receiver = User.objects.get(username = receiver)
        group = Group.objects.get(name = groupname)            
        if receiver in group.members.all():
            result = schema.execute(query)
            if result.errors:
                return Response({'errors': [str(error) for error in result.errors]}, status=status.HTTP_400_BAD_REQUEST)
            return Response(result.data['userReceivedgroupmessages'])
        else:
            return Response({'error': 'Only group members can see the messages.'}, status=status.HTTP_403_FORBIDDEN)
        
        



# {
#     "username" : "admin2",
#     "password" : "admin2"
# }