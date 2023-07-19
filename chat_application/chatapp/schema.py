import graphene
from graphene_django import DjangoObjectType
from .models import User, Group, Message, GroupMessage


# types

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = '__all__'

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = '__all__'

class GroupMessageType(DjangoObjectType):
    class Meta:
        model = GroupMessage
        fields = '__all__'


# Query

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_groups = graphene.List(GroupType)
    user_receivedMessages = graphene.List(MessageType, sender=graphene.String(required=True), receiver=graphene.String(required=True))
    user_receivedGroupMessages = graphene.List(GroupMessageType,  groupName=graphene.String(required=True))


    def resolve_all_users(self, info):
        return User.objects.all()
    
    def resolve_all_groups(self, info):
        return Group.objects.all()
    
    def resolve_user_receivedMessages(self, info, sender, receiver):
        sender = User.objects.get(username=sender)
        receiver = User.objects.get(username=receiver)
        messages = Message.objects.filter(sender=sender, receiver=receiver)
        return messages 
    
    def resolve_user_receivedGroupMessages(self, info, groupName):        
        group = Group.objects.get(name=groupName)        
        group_messages = GroupMessage.objects.filter(group=group)        
        return group_messages
        

# message mutation
class CreateMessageMutation(graphene.Mutation):
    message = graphene.Field(MessageType)
    success = graphene.Boolean()

    class Arguments:
        sender_name = graphene.String(required=True)
        receiver_name = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_name, receiver_name, content):
        sender = User.objects.get(username=sender_name)
        receiver = User.objects.get(username=receiver_name)
        message = Message(sender=sender, receiver=receiver, content=content)
        message.save()
        return CreateMessageMutation(success=True, message=message)
    
    # group message mutation
class CreateGroupMessageMutation(graphene.Mutation):
    message = graphene.Field(GroupMessageType)
    success = graphene.Boolean()

    class Arguments:
        sender_name = graphene.String(required=True)
        group_name = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_name, group_name, content):
        sender = User.objects.get(username=sender_name)
        group = Group.objects.get(name=group_name)
        message = GroupMessage(sender=sender, group=group, content=content)
        message.save()
        return CreateGroupMessageMutation(success=True, message=message)
        

# mutation
class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_groupmessage = CreateGroupMessageMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)