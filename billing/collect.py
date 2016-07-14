from billing.models import Plan, Customer, Invoice

from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

import time

CHARGE_DEADLINE = 432000
WARNING_DEADLINE = 172800
DOWNGRADE_DEADLINE = 0

def batch_update_customers():
    for customer in Customer.objects.filter(
        expiry_timestamp__lt=int(time.time()) + CHARGE_DEADLINE,
        expiry_timestamp__gt=0
    ):
        invoices = customer.invoices.filter(paid=False, amount_cents=customer.plan.price_cents)
        if invoices.count() == 0:
            customer.invoices.filter(paid=False).delete()
            invoice = Invoice()
            invoice.customer = customer
            invoice.amount_cents = customer.plan.price_cents
            invoice.save()
            if len(customer.stripe_id) > 0:
                print "CHARGE STRIPE %s" % customer.user.username
                try:
                    stripe.Charge.create(
                        amount=customer.plan.price_cents, # in cents
                        currency="usd",
                        customer=customer.stripe_id,
                        description="Acacia: %s Plan payment" % customer.plan.name
                    )
                    invoice.paid = True
                    invoice.paid_timestamp = int(time.time())
                    invoice.save()
                    customer.expiry_timestamp = int(time.time()) + 2592000
                    customer.save()
                except Exception:
                    customer.stripe_id = ""
                    customer.save()
            
            if not invoice.paid:
                if not invoice.creation_email_sent:
                    print "INVOICE EMAIL %s" % customer.user.username
                    invoice.send_creation_email()
        else:
            invoice = invoices[0]
            delete = [x.delete() for x in invoices[1:]]
            if customer.expiry_timestamp < int(time.time()) + WARNING_DEADLINE and not invoice.warning_email_sent:
                invoice.send_warning_email()
                print "WARNING EMAIL %s" % customer.user.username    
            elif customer.expiry_timestamp < int(time.time()):
                print "DOWNGRADE %s" % customer.user.username
                plan = Plan.objects.all().order_by('price_cents')[0]
                customer.plan = plan
                customer.expiry_timestamp = -1
                customer.save()
                
                bots = customer.user.bots.all()[plan.num_bots_allowed:]
                for bot in bots:
                    bot.delete()
                    
                customer.invoices.all().delete()
                send_downgrade_email(customer)
                

def send_downgrade_email(customer):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    email_content = render_to_string(
        "billing/email_downgrade.txt",
        context={"username":customer.user.username}
    )

    result = send_mail(
        'Acacia Account Downgraded',
        email_content,
        'noreply@tradeacacia.com',
        [customer.user.email],
        fail_silently=True
    )
    return result == 1