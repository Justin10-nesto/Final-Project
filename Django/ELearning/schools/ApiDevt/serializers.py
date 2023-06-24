from rest_framework import serializers
from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking

class TutorialTimeTackingSerializer(serializers.ModelSerializer):

    class Meta:
        model =TutorialTimeTacking
        fields = '_all_'