from django.db import models

# Create your models here.
class EmailLevel(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.level_desc


class EmailType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.type_desc

class Announcement(models.Model):
    email_level = models.ForeignKey(EmailLevel, on_delete=models.CASCADE)
    email_type = models.ForeignKey(EmailType, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject