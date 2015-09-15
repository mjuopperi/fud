from django.db import models

NOT_ALLOWED_SUBDOMAINS = [
	'static', 
	'www', 
	'api', 
]

def validate_subdomain(subdomain):
	if subdomain in NOT_ALLOWED_SUBDOMAINS:
		raise ValidationError('%s is not allowed subdomain' % subdomain)
	if subdomain != subdomain.lower():
		raise ValidationError('Only lovercase letters')

class Restaurant(models.Model):
	name = models.CharFiend(max_length=255)
	subdomain = models.CharFiend(max_length=255, unique=True, validators=[validate_subdomain])
	address = models.CharField(max_length=255, null=True, blank=True, default=None)
	postal_code = models.CharField(max_length=5, null=True, blank=True, default=None)
	city = models.CharField(max_length=45, null=True, blank=True, default=None)
	phone_number = models.CharField(max_length=32, null=True, blank=True, default=None)
	public_email = models.EmailField(null=True, blank=True, default=None)
	contact_email = models.EmailField()
	#admins = models.TODO
	#owner = models.TODO

class MenuCategory(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField(max_length=80)

class MenuItem(models.Model):
	category = models.ForeignKey(MenuCategory)
	title = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True, default=None)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	allergies = models.TextField(null=True, blank=True, default=None)
