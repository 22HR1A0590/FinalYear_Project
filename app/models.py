from django.db import models
import os
# Create your models here.

class UserModel(models.Model):
    ROLE_CHOICES = (
        ('do', 'Data Owner'), ('du', 'Data User')
        )
    
    username=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    contact=models.CharField(max_length=15, null=True)
    address=models.TextField(blank=True)
    profile=models.ImageField(upload_to=os.path.join('Profile') , null=True)

    def __str__(self):
        return self.username
    
    class Meta():
        db_table='UserModel'
        


class Document(models.Model):
    filename = models.CharField(max_length=30)
    file = models.FileField(upload_to=os.path.join('static/assets','Files'))
    filedata=models.BinaryField()
    keyword = models.CharField(max_length=50)  # lowercase here
    encrypted_keyword = models.TextField()     # singular and consistent
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)



    def __str__(self):
        return self.filename
    
    class Meta:
        db_table='Document'


class RequestFile(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE)
    owner=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    requester_email = models.EmailField(null=True)
    status=models.CharField(max_length=20, choices=[('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')], default='pending')
    download_key=models.CharField(max_length=10 , null=True , blank=True)
    class Meta:
        db_table='RequestFile'



class Server_A(models.Model):
    file_part=models.TextField()
    doc_id=models.IntegerField()
    keyword=models.CharField(max_length=100 , null=True)

    class Meta():
        db_table='Server_A'

class Server_B(models.Model):
    file_part=models.TextField()
    doc_id=models.IntegerField()
    keyword=models.CharField(max_length=100 , null=True)
    

    class Meta():
        db_table='Server_B'

class Server_C(models.Model):
    file_part=models.TextField()
    doc_id=models.IntegerField()
    keyword=models.CharField(max_length=100 , null = True)

    class Meta:
        db_table='Server_C'

