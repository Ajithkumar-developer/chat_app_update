from django.db import models

# Create your models here.
# user model
class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.username
    
# group model
class Group(models.Model):
    name = models.CharField(max_length=25, unique=True)
    members = models.ManyToManyField(User, related_name='groups')

    def __str__(self):
        return self.name
    
# message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From: {self.sender} | To: {self.receiver} | Content: {self.content}"
        

    
# group message model
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_sender')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Group: {self.group} | Sender: {self.sender} | Content: {self.content}"