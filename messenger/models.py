from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
  user = models.ForeignKey(
    to=User,
    on_delete=models.DO_NOTHING,
    related_name='user_to',
  )
  author = models.ForeignKey(
    to=User,
    on_delete=models.DO_NOTHING,
    related_name='msg_author',
  )
  text = models.CharField(
    max_length=500,
  )
  pub_date = models.DateTimeField(
    auto_now_add=True,
  )

  def __str__(self):
    return f"{self.author.username} -> {self.user.username}: {self.text}"
