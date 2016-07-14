from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import View, ListView
from billing.models import Plan, Invoice

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

import time

from billing.utils import billing_check, BillingCheckMixin

# Create your views here.
class PlanList(BillingCheckMixin, ListView):
    model = Plan
    
    def get_context_data(self, **kwargs):
        context = super(PlanList, self).get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        return context
    
    def get_queryset(self):
        return Plan.objects.all().order_by("price_cents")
    
    
@login_required
@user_passes_test(billing_check)
def index(request):
    return render(
        request,
        "billing/index.html",
        {
            "invoices":request.user.customer.invoices.all().order_by("-pk"),
            "free_plan":Plan.objects.filter(price_cents=0)[0]
        }
    )

class PayInvoice(View):
    def get(self, request, invoice_id):
        invoices = Invoice.objects.filter(pk=invoice_id)
        if invoices.count() != 1:
            return HttpResponse("Invoice is paid or does not exist.")
        else:
            invoice = invoices[0]
            if invoice.paid:
                return render(request, "billing/pay_invoice_done.html", {"invoice":invoice})
            else:
                return render(
                    request,
                    "billing/pay_invoice.html",
                    {
                        "stripe_pk":settings.STRIPE_PUBLIC_KEY,
                        "invoice":invoices[0]
                    }
                )
    
    def post(self, request, invoice_id):
        # check if invoice exists (and is paid)
        # attempt to pay invoice => use switch_plan logic (upgrade / extend only)
            # if invoice: mark invoice as paid
        invoices = Invoice.objects.filter(pk=invoice_id, paid=False)
        if invoices.count() != 1:
            return HttpResponse("Invoice is paid or does not exist.")
        else:
            invoice = invoices[0]
            c = invoice.customer
            plan = c.plan
            p = request.POST
            charge_description = "Acacia: %s Plan payment" % plan.name
            
            if not p.get("stripeToken") or not p.get("stripeTokenType"):
                messages.error(request, "Missing payment parameters for request.")
                return redirect("billing:pay_invoice")
            else:
                # create a charge and create a Stripe customer object if card
                token = p["stripeToken"]
                if p["stripeTokenType"] == "card":
                    try:
                        customer = stripe.Customer.create(
                            source=token,
                            description=c.user.email
                        )
                        print customer.id
                        c.stripe_id = customer.id
                        c.save()
                    except stripe.error.CardError, e:
                        messages.error(request, "An unkown error ocurred. Please contact support.")
                        return redirect("billing:pay_invoice")

                    try:
                        stripe.Charge.create(
                            amount=invoice.amount_cents, # in cents
                            currency="usd",
                            customer=c.stripe_id,
                            description=charge_description
                        )
                    except stripe.error.CardError, e:
                        messages.error(request, "Your card was declined. Please update your billing information.")
                        return redirect("billing:pay_invoice")
                else:
                    try:
                        stripe.Charge.create(
                            amount=invoice.amount_cents, # in cents
                            currency="usd",
                            source=token,
                            description=charge_description
                        )
                    except stripe.error.CardError, e:
                        messages.error(request, "An error ocurred with your payment.  Please try again.")
                        return redirect("billing:pay_invoice")
            
            invoice.paid = True
            invoice.paid_timestamp = int(time.time())
            invoice.save()
            
            c.expiry_timestamp = int(time.time()) + 2592000
            c.save()
            return self.get(request, invoice.pk)
        
@login_required
@user_passes_test(billing_check)
def switch_plan(request, plan_id_str):
    plan_id = int(plan_id_str)
    c = request.user.customer
    
    if plan_id == c.plan.pk:
        messages.warning(request, "You already own that subscription.")
        return redirect("billing:plan_list")
    elif plan_id not in [x.pk for x in list(Plan.objects.all())]:
        messages.warning(request, "Invalid subscription.")
        return redirect("billing:plan_list")
    else:
        # get plan object & upgrade
        plan = Plan.objects.get(pk=plan_id)
        charge_description = "Acacia: %s Plan payment" % plan.name
        
        if plan.price_cents > 0:
            if request.method == "GET":
                if len(c.stripe_id) == 0:
                    # invalid stripe ID for customer
                    messages.error(request, "You must enter your payment information.")
                    return redirect("billing:plan_list")
                else:
                    # charge customer's current card
                    try:
                        stripe.Charge.create(
                            amount=plan.price_cents, # in cents
                            currency="usd",
                            customer=c.stripe_id,
                            description=charge_description
                        )
                    except Exception:
                        c.stripe_id = ""
                        c.save()
                        messages.error(request, "Payment failed. Please try again.")
                        return redirect("billing:plan_list")

            elif request.method == "POST":
                p = request.POST
                if not p.get("stripeToken") or not p.get("stripeTokenType"):
                    messages.error(request, "Missing payment parameters for request.")
                    return redirect("billing:plan_list")
                else:
                    # create a charge and create a Stripe customer object if card
                    token = p["stripeToken"]
                    if p["stripeTokenType"] == "card":
                        try:
                            customer = stripe.Customer.create(
                                source=token,
                                description=request.user.email
                            )
                            print customer.id
                            c.stripe_id = customer.id
                            c.save()
                        except stripe.error.CardError, e:
                            messages.error(request, "An unkown error ocurred. Please contact support.")
                            return redirect("billing:plan_list")

                        try:
                            stripe.Charge.create(
                                amount=plan.price_cents, # in cents
                                currency="usd",
                                customer=c.stripe_id,
                                description=charge_description
                            )
                        except stripe.error.CardError, e:
                            messages.error(request, "Your card was declined. Please update your billing information.")
                            return redirect("billing:plan_list")
                    else:
                        try:
                            stripe.Charge.create(
                                amount=plan.price_cents, # in cents
                                currency="usd",
                                source=token,
                                description=charge_description
                            )
                        except stripe.error.CardError, e:
                            messages.error(request, "An error ocurred with your payment.  Please try again.")
                            return redirect("billing:plan_list")
                        
                        
            invoice = Invoice()
            invoice.customer = c
            invoice.amount_cents = plan.price_cents
            invoice.paid = True
            invoice.paid_timestamp = int(time.time())
            invoice.save()
        
        # change user's payment plan & update deadline timestamp
        c.plan = plan
        c.expiry_timestamp = time.time() + 2592000 #30 days
        if plan.price_cents == 0:
            c.expiry_timestamp = -1
        c.save()
        bots = request.user.bots.all()[plan.num_bots_allowed:]
        for bot in bots:
            bot.delete()
            
        messages.success(request, "Subscription successfully updated.")
        return redirect("main:index")