from django.db import models



class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    born_date = models.DateField(null=True, blank=True)
    born_location = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    quote = models.TextField()

    def __str__(self):
        return f"{self.quote}"