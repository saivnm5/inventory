from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker


class Item(models.Model):
	name = models.CharField(max_length=255)
	brand = models.CharField(max_length=255)
	category = models.CharField(max_length=255)
	product_code = models.CharField(max_length=13)
	last_user = models.CharField(max_length=255, default='admin')
	tracker = FieldTracker()

	def __str__(self):
		return self.name


class Variant(models.Model):
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	selling_price = models.DecimalField(max_digits=6, decimal_places=2)
	cost_price = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.IntegerField()
	is_active = models.BooleanField(default=True)
	last_user = models.CharField(max_length=255, default='admin')
	tracker = FieldTracker()

	def __str__(self):
		return self.name


class VariantProperty(models.Model):
	# using EAV model
	variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
	property = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	last_user = models.CharField(max_length=255, default='admin')
	is_active = models.BooleanField(default=True)
	tracker = FieldTracker()

	def __str__(self):
		return (self.variant.name+' '+self.property+': '+self.value)


class ItemChangeLog(models.Model):
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	attribute = models.CharField(max_length=255)
	variant = models.ForeignKey(Variant, null=True, on_delete=models.PROTECT)
	old_value = models.CharField(max_length=255)
	new_value = models.CharField(max_length=255)
	user = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)


class VariantChangeLog(models.Model):
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
	attribute = models.CharField(max_length=255)
	is_property_change = models.BooleanField(default=False)
	property = models.ForeignKey(VariantProperty, null=True, on_delete=models.PROTECT)
	old_value = models.CharField(max_length=255)
	new_value = models.CharField(max_length=255)
	user = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Item)
def item_change_logger(sender, instance, created, raw, using, update_fields, **kwargs):
	
	if not created:
		if instance.tracker.has_changed('name'):
			log = ItemChangeLog(item=instance, attribute='name', user=instance.last_user)
			log.new_value = instance.name 
			log.old_value = instance.tracker.previous('name')
			log.save()

		if instance.tracker.has_changed('brand'):
			log = ItemChangeLog(item=instance, attribute='brand', user=instance.last_user)
			log.new_value = instance.brand 
			log.old_value = instance.tracker.previous('brand')
			log.save()

		if instance.tracker.has_changed('category'):
			log = ItemChangeLog(item=instance, attribute='category', user=instance.last_user)
			log.new_value = instance.category 
			log.old_value = instance.tracker.previous('category')
			log.save()


@receiver(post_save, sender=Variant)
def variant_change_logger(sender, instance, created, raw, using, update_fields, **kwargs):
	
	if created:
		log = ItemChangeLog(item=instance.item, variant=instance, attribute='variant', user=instance.last_user)
		log.new_value = True
		log.old_value = False
		log.save()

	if not created:
		if instance.tracker.has_changed('name'):
			log = VariantChangeLog(item=instance.item, variant=instance, attribute='name', user=instance.last_user)
			log.new_value = instance.name 
			log.old_value = instance.tracker.previous('name')
			log.save()

		if instance.tracker.has_changed('selling_price'):
			log = VariantChangeLog(item=instance.item, variant=instance, attribute='selling_price', user=instance.last_user)
			log.new_value = str(instance.selling_price)
			log.old_value = str(instance.tracker.previous('selling_price'))
			log.save()

		if instance.tracker.has_changed('cost_price'):
			log = VariantChangeLog(item=instance.item, variant=instance, attribute='cost_price', user=instance.last_user)
			log.new_value = str(instance.cost_price )
			log.old_value = str(instance.tracker.previous('cost_price'))
			log.save()

		if instance.tracker.has_changed('quantity'):
			log = VariantChangeLog(item=instance.item, variant=instance, attribute='quantity', user=instance.last_user)
			log.new_value = instance.quantity 
			log.old_value = instance.tracker.previous('quantity')
			log.save()

		if instance.tracker.has_changed('is_active'):
			log = ItemChangeLog(item=instance.item, variant=instance, attribute='variant', user=instance.last_user)
			log.new_value = instance.is_active
			log.old_value = instance.tracker.previous('is_active')
			log.save()


@receiver(post_save, sender=VariantProperty)
def variant_property_change_logger(sender, instance, created, raw, using, update_fields, **kwargs):

	if created:
		log = VariantChangeLog(item=instance.variant.item, variant=instance.variant, attribute='property', property=instance, is_property_change=True, user=instance.last_user)
		log.new_value = True
		log.old_value = False
		log.save()

	if not created:
		if instance.tracker.has_changed('property'):
			log = VariantChangeLog(item=instance.variant.item, variant=instance.variant, attribute='property', property=instance, is_property_change=True, user=instance.last_user)
			log.new_value = instance.property
			log.old_value = instance.tracker.previous('property')
			log.save()

		if instance.tracker.has_changed('value'):
			log = VariantChangeLog(item=instance.variant.item, variant=instance.variant, attribute='property', property=instance, user=instance.last_user)
			log.new_valaue = instance.value
			log.old_value = instance.tracker.previous('value')
			log.save()

		if instance.tracker.has_changed('is_active'):
			log = VariantChangeLog(item=instance.variant.item, variant=instance.variant, attribute='property', property=instance, is_property_change=True, user=instance.last_user)
			log.new_value = instance.is_active
			log.old_value = instance.tracker.previous('is_active')
			log.save()