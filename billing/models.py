from django.db import models

from django.contrib.auth.models import User

import time
import datetime

# Create your models here.

class Plan(models.Model):
    price_cents = models.IntegerField()
    name = models.CharField(max_length=15)
    
    num_bots_allowed = models.IntegerField()
    max_trade_size_usd = models.FloatField()
    
    def __str__(self):
        return self.name
    
    def price_string(self):
        return "$%s" % (self.price_cents / 100)
    
    def trade_size_string(self):
        return "$%s" % int(self.max_trade_size_usd)


class Customer(models.Model):
    user = models.OneToOneField(User, related_name="customer")
    plan = models.ForeignKey(Plan, related_name="subscribers")
    
    # Only used for people with cards
    stripe_id = models.CharField(max_length=100, default="", blank=True)
    
    expiry_timestamp = models.IntegerField()
    
    def can_add_more_bots(self):
        return self.plan.num_bots_allowed > self.user.bots.all().count() or \
            self.plan.num_bots_allowed == -1
    
    
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, related_name="invoices")
    
    amount_cents = models.IntegerField()
    paid = models.BooleanField(default=False)
    paid_timestamp = models.IntegerField(default=0)
    
    creation_email_sent = models.BooleanField(default=False)
    warning_email_sent = models.BooleanField(default=False)
    
    def send_creation_email(self):
        if self.send_email("creation"):
            self.creation_email_sent = True
        self.save()
    
    def send_warning_email(self):
        if self.send_email("warning"):
            self.warning_email_sent = True
        self.save()
    
    def send_email(self, email_type):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        
        email_content = render_to_string(
            "billing/invoice_%s.txt" % email_type,
            context={
                "username":self.customer.user.username,
                "amount":self.amount_string(),
                "due_date":datetime.datetime.fromtimestamp(
                    self.customer.expiry_timestamp
                ).strftime('%B %-d'),
                "invoice_id":self.pk,
                "base_url":settings.BASE_URL
            }
        )
        
        result = send_mail(
            'Your Acacia Invoice',
            email_content,
            'noreply@tradeacacia.com',
            [self.customer.user.email],
            fail_silently=True
        )
        return result == 1
    
    def amount_string(self):
        return "$%s" % (self.amount_cents / 100)
    
    def paid_string(self):
        return datetime.datetime.fromtimestamp(
            self.paid_timestamp
        ).strftime('%b %-d, %Y, %-I:%M %p')