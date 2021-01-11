from django.db import models
# Create your models here.

class Admin(models.Model):
    id = models.IntegerField(primary_key=True,default='')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username

class Candidate(models.Model):
    GENDER = (('MALE','MALE'),('FEMALE','FEMALE'),)
    YEAR = ((1,1),(2,2),(3,3),(4,4),)
    POSITION = (('SECRETARY','SECRETARY'),('ASSISTANT SECRETARY','ASSISTANT SECRETARY'),
                ('PRESIDENT','PRESIDENT'),('VICE PRESIDENT','VICE PRESIDENT'),)
    DEPT = (('COMPUTER SCIENCE','COMPUTER SCIENCE'),('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
            ('ELECTRONICS','ELECTRONICS'),('MECHANICAL','MECHANICAL'),('ELECTRICAL','ELECTRICAL'),)

    CRegistration_Id = models.IntegerField(primary_key=True)
    Cname = models.CharField(max_length=40)
    Cgender = models.CharField(max_length=40,choices=GENDER)
    Cdept = models.CharField(max_length=40,choices=DEPT,null=True)
    Cyear = models.IntegerField(choices=YEAR)
    Cusername = models.CharField(max_length=40,unique=True)
    Cpassword = models.CharField(max_length=40,unique=True)
    Cmobile_no = models.PositiveBigIntegerField()
    Cemail_id = models.EmailField(unique=True)
    Cposition = models.CharField(max_length=40,choices=POSITION)
    admin = models.ForeignKey(Admin,null=True,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default='')
    def __str__(self):
        return self.Cname

class AcceptedCandidates(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

class Voter(models.Model):
    GENDER = (('MALE','MALE'),('FEMALE','FEMALE'),)
    YEAR = ((1,1),(2,2),(3,3),(4,4),)
    DEPT = (('COMPUTER SCIENCE','COMPUTER SCIENCE'),('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
            ('ELECTRONICS','ELECTRONICS'),('MECHANICAL','MECHANICAL'),('ELECTRICAL','ELECTRICAL'),)

    VRegistration_Id = models.IntegerField(primary_key=True)
    Vname = models.CharField(max_length=40)
    Vgender = models.CharField(max_length=40,choices=GENDER)
    Vdept = models.CharField(max_length=40,choices=DEPT,null=True)
    Vyear = models.IntegerField(choices=YEAR)
    Vusername = models.CharField(max_length=40,unique=True)
    Vpassword = models.CharField(max_length=40,unique=True)
    Vmobile_no = models.PositiveBigIntegerField()
    Vemail_id = models.EmailField(unique=True)
    admin = models.ForeignKey(Admin,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.Vname

class VotedLists(models.Model):
    votedcandidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)

class Election(models.Model):
    POSITION = (('SECRETARY','SECRETARY'),('ASSISTANT SECRETARY','ASSISTANT SECRETARY'),
                ('PRESIDENT','PRESIDENT'),('VICE PRESIDENT','VICE PRESIDENT'))

    e_Id = models.IntegerField(primary_key=True)
    e_position = models.CharField(max_length=40,unique=True,choices=POSITION)
    e_title = models.CharField(max_length=100)
    e_date = models.DateField()
    admin = models.ForeignKey(Admin,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.e_title

class WinnerList(models.Model):
    candidates = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    totalvote = models.IntegerField()