from django.db import models

class DefaultUsers(models.Model):
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school_selected = models.TextField()
    course = models.TextField()
    type = models.CharField(max_length=255)   
    location = models.CharField(max_length=255)
     
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'DefaultUsers'
        
class Subject(models.Model):
    subject_code = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.subject_name

class NotesFiles(models.Model):
    title_of_documment = models.CharField(max_length=50)
    type_of_the_book = models.CharField(max_length=50)
    documment = models.FileField(upload_to=None )
    
    def __str__(self):
        return self.subject_name
 
class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField(null=True)
    
    def __str__(self):
        return self.title

class Topics(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    marks = models.BigIntegerField()
    notes =models.ForeignKey(Notes, on_delete = models.CASCADE)
    file =models.ForeignKey(NotesFiles, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
    
class SubTopic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    marks = models.BigIntegerField()
    subject = models.ForeignKey(Topics, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class QuestionType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.ForeignKey(QuestionType, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class AssigmentType(models.Model):
    name = models.CharField(max_length=50)
    weight = models.BigIntegerField()
    
    def __str__(self):
        return self.name
    
class Assigment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    comment = models.TextField(null=True)
    subtopic = models.OneToOneField(SubTopic, on_delete = models.CASCADE)
    status = models.ForeignKey(Status, on_delete= models.CASCADE)
    type = models.ForeignKey(AssigmentType, on_delete= models.CASCADE)

    
    def __str__(self):
        return self.name
    
class StudentGroupType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'StudentGroupType'
        

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("StudentGroupType_detail", kwargs={"pk": self.pk})

class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    type = models.ForeignKey(StudentGroupType, on_delete= models.CASCADE)
    assignent = models.ForeignKey(Assigment, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("StudentGroup_detail", kwargs={"pk": self.pk})
    
class Student(models.Model):
    name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})
