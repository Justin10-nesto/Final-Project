from rest_framework import serializers
from schools.models import Subject
from OnlineLearning.models import TutorialTimeTacking

class TutorialTimeTackingSerializer(serializers.ModelSerializer):

    class Meta:
        model =TutorialTimeTacking
        fields = '_all_'
        
class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model =Subject
        fields = '_all_'