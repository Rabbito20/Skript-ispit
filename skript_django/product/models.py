from io import BytesIO
from os import name
from PIL import Image

from django.core.files import File
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)  # Naziv kategorije
    slug = models.SlugField()  # Adresa naziva

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    #   ForeignKet je id u bazi (relacioni kljuc)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    # Autmoatski se updateuje svakim novim dodavanjem u bazu
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ovaj "-" znaci da ce biti poredjano u opadajucem redosledu po datumu azuriranja/dodavanja
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')  # Cisto da se osiguramo da je sve ok sa slikom
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)  # Probaj sa PNG-om isto

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
