from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    birth_date = models.DateField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, default='photos/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street

    class Meta:
        ordering = ['street']


class Contact(models.Model):
    KINDS = (
        ('P', 'Phone'),
        ('E', 'Email'),
    )
    kind = models.CharField(max_length=1, choices=KINDS)
    value = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value

    class Meta:
        ordering = ['kind']
