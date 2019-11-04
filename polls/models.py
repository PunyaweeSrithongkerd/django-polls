import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


def vote_count(id):
    total_vote = 0
    for choice in Question.objects.get(pk=id).choice_set.all():
        total_vote += choice.votes
    return total_vote


def find_polls_for_text(text):
    """Return list of Question objects for all polls containing some text"""
    # Hint: Question.objects.filter( expression )
    # and use the relations question_text__contains or __icontains
    return Question.objects.filter(question_text__contains = text)