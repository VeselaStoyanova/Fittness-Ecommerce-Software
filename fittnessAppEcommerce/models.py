from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    password = models.TextField(blank=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    years = models.IntegerField()

    def __str__(self):
        return "Customer: {}".format(self.firstName, self.lastName, self.password,
                                self.username, self.email,
                                self.gender, self.years)


class TrainingMode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shortDescription = models.TextField(blank=True)
    longDescription = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    TRAINING_MODE_CHOICE = (
        ('L', 'Loosing weight'),
        ('M', 'Maintaining weight'),
        ('G', 'Gaining weight'),
        ('S', 'Stretching'),
    )
    category = models.CharField(max_length=1, choices=TRAINING_MODE_CHOICE)
    objects = models.Manager

    def __str__(self):
        return "Training mode: {}".format(self.name, self.shortDescription, self.longDescription,
                                          self.price, self.duration, self.category)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Diet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    calories = models.IntegerField()
    proteins = models.IntegerField()
    carbohydrates = models.IntegerField()
    fats = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    DIET_CHOICE = (
        ('L', 'Loosing weight'),
        ('M', 'Maintaining weight'),
        ('G', 'Gaining weight')
    )

    category = models.CharField(max_length=1, choices=DIET_CHOICE)
    objects = models.Manager

    def __str__(self):
        return "Diet: {}".format(self.name, self.description, self.price,
                                 self.calories, self.proteins, self.carbohydrates,
                                 self.fats, self.category)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    PRODUCT_CHOICE = (
        ('PP', 'Protein powder'),
        ('ED', 'Energy drinks'),
        ('PB', 'Protein bar'),
        ('V', 'Vitamins'),
    )
    category = models.CharField(max_length=2, choices=PRODUCT_CHOICE)
    calories = models.IntegerField()
    description = models.TextField(blank=True)
    objects = models.Manager

    def __str__(self):
        return "Product: {}".format(self.name, self.price, self.category,
                                    self.calories, self.description)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return "Order: {}".format(self.customer, self.date_ordered, self.complete, self.transaction_id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for item in orderitems:
			# if, a product is not digital, then it has to be shipped
			if item.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	training = models.ForeignKey(TrainingMode, on_delete=models.SET_NULL, null=True)
	diet = models.ForeignKey(Diet, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "ShippingAddress: {}".format(self.customer, self.order, self.address,
                                            self.city, self.state, self.state,
                                            self.zipcode, self.date_added)
