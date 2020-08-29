from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, )
    mobile = models.CharField(max_length=11, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.email, self.message[0:50])

    # def get_absolute_url(self):
    #    return reverse('contact')
