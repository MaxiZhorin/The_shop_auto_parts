from django.db import models

class ProductGroup(models.Model):
    name = models.CharField(max_length=64, blank=True, default='group')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Группа %s' % (self.name )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class ProductGroupImage(models.Model):
    group = models.ForeignKey(ProductGroup, blank=True, null=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image_group/')
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=True)

    def __str__(self):
        return 'Товар %s' % (self.id)

    class Meta:
        verbose_name = 'фотография группы'
        verbose_name_plural = 'фотографии групп '

class Product (models.Model):
    customer_name = models.CharField(max_length=64, blank= True, null= True,default= None)
    price = models.DecimalField(max_digits=100, decimal_places=2,blank= False, default=0)
    descripton = models.TextField(blank= True, null= True,default= None)
    vendor = models.CharField(max_length=64, blank= True, null= True,default= None)
    article = models.CharField(max_length=100, blank= True, null= True,default= None)
    group = models.ForeignKey(ProductGroup, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add= True, auto_now= False)
    updated = models.DateTimeField(auto_now_add= False, auto_now= True)


    def __str__(self):
        return 'Товар %s %s' % (self.customer_name, self.article)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage (models.Model):
     product = models.ForeignKey(Product, blank= True, null= True,default= None, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='product_image/',default='product_image/default.jpg')
     is_active = models.BooleanField(default= True)
     is_main = models.BooleanField(default=False)



     def __str__(self):
        return 'Товар %s' % (self.id)

     class Meta:
       verbose_name = 'фотография'
       verbose_name_plural = 'фотографии '


class ProductCross(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    cross = models.CharField(max_length=100, blank= True, null= True,default= None)

    def __str__(self):
        return 'Кросс артикула %s' % (self.cross)

    class Meta:
        verbose_name = 'Кросс артикула'
        verbose_name_plural = 'Кроссы '


