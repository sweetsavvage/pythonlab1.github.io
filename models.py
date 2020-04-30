from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now

class Message(models.Model):
    author = models.ForeignKey(User, verbose_name="От кого", on_delete=models.CASCADE, related_name="author_to_user" )
    recipient = models.ForeignKey(User, verbose_name='Кому', on_delete=models.CASCADE, related_name="recipient_to_user")
    subject = models.CharField(max_length=50, verbose_name='Тема')
    text = models.TextField("Текст сообщения")
    pub_date = models.DateTimeField('Дата', default=now)

    class Meta:
        ordering=['pub_date']

    def str(self):
        return "From {} to {} : ".format(author,recipient,subject)
