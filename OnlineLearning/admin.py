from django.contrib import admin
from OnlineLearning.models import Teacher,  Student,AnnouncimentType,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany, StudentTask

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(AnnouncimentType)
admin.site.register(GroupPost)
admin.site.register(GroupPostComent)
admin.site.register(GroupPostLike)
admin.site.register(StudentSubject)
admin.site.register(Announciment)
admin.site.register(Notes)
admin.site.register(DefaultUsers)
admin.site.register(Tutorial)
admin.site.register(GroupDiscussionsMessage)
admin.site.register(GroupDiscussionReply)
admin.site.register(Book)
admin.site.register(Assigment)
admin.site.register(StudentGroup)
admin.site.register(StudentGroupType)
admin.site.register(AssigmentType)
admin.site.register(Topic)
admin.site.register( AssigmentSubmission)
admin.site.register(StudentClassManyToMany)
admin.site.register(StudentTask)