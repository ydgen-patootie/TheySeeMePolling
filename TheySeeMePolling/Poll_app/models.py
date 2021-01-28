from django.db import models



class Poll(models.Model):
    name = models.CharField(max_length=150)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return "Poll " + self.name    
    
    
class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    
    qtypes = (('TA','Text answer'),('PO', "Pick one"),('PA', "Pick any"))
    qtype = models.CharField(max_length=2, choices=qtypes)

    def __str__(self):
        return "Question " + self.text 
    
    
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice = models.CharField(max_length=150)

    def __str__(self):
        return "Choice " + self.choice
    
    
class Answer(models.Model):
    user_id = models.IntegerField()
    poll = models.ForeignKey(Poll, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='answers', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "Answer " + self.answer