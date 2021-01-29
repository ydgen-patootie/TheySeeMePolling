from rest_framework import serializers
from .models import Poll, Question, Choice, Answer


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class Answer_Serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True)
    answer = serializers.CharField(max_length=150, allow_null=True, allow_blank=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def validate(self, attrs):
        try:
            obj = Answer.objects.get(user_id=attrs['user_id'],poll=attrs['poll'].id, question=attrs['question'].id, choice=attrs['choice'], answer=attrs['answer'])
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Answer to this question with this parameters exists')        


class Choice_Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.CharField(max_length=150)

    def validate(self, attrs):
        try:
            obj = Choice.objects.get(question=attrs['question'].id, choice=attrs['choice'])
        except Choice.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Choice with this name exists')

    class Meta:
        model = Choice
        fields = '__all__'

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class Question_Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    text = serializers.CharField(max_length=500)
    qtype = serializers.CharField(max_length=2)
    choices = Choice_Serializer(many=True, read_only=True)

    def validate(self, attrs):
        qtype = attrs['qtype']
        if qtype in ('TA','PO','PA'):
            return attrs
        raise serializers.ValidationError('Unexpected value in qtype. Use TA, PO, PA')

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class Poll_Serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    description = serializers.CharField(max_length=500, required=False)
    questions = Question_Serializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'start_date' in validated_data:
            raise serializers.ValidationError({'start_date': 'This field may be set only during creation'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
