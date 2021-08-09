from rest_framework import serializers
from Usertask.models import Task , TaskUser



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
        
            

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
    
class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUser
        fields = '__all__'
        
        
            

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return TaskUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.task = validated_data.get('task', instance.task)
        instance.email = validated_data.get('email', instance.email)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    