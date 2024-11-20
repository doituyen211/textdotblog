from django.db import models
import datetime


class DotUseHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True, blank=True)
    dot = models.ForeignKey('Dots', models.DO_NOTHING, null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"History ID: {self.history_id}, User: {self.user}, Dot: {self.dot}"

    class Meta:
        db_table = 'dot_use_history'


class Dots(models.Model):
    dot_id = models.AutoField(primary_key=True)
    dot_name = models.CharField(max_length=150, help_text="Dot's name", default="Dot")
    input_text = models.TextField()
    output_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    completed_at = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=255, null=True, blank=True)

    DOT_TYP = (
        ('w', 'WRITE'),
        ('r', 'REWRITE'),
        ('s', 'SUMMARIZE'),
    )

    dot_type = models.CharField(max_length=1, choices=DOT_TYP, default='w', null=True, blank=True,
                                help_text='Type of Dot')

    def save(self, *args, **kwargs):
        if not self.dot_name:
            self.dot_name = self.input_text[:150]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dot ID: {self.dot_id}, Name: {self.dot_name}"

    class Meta:
        db_table = 'dots'


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True, blank=True)
    plan = models.ForeignKey('PricePlan', models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=datetime.datetime.now)

    PAYMENT_STA = (
        ('c', 'COMPLETED'),
        ('p', 'PENDING'),
        ('f', 'FAILED'),
    )

    CARD_TYP = (
        ('cc', 'CREDIT CARDS'),
        ('dc', 'DEBIT CARDS'),
        ('pc', 'PRE-PAID CARDS'),
    )

    payment_status = models.CharField(max_length=1, choices=PAYMENT_STA, null=True, blank=True)
    card_type = models.CharField(max_length=2, choices=CARD_TYP, null=True, blank=True)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, User: {self.user}, Amount: {self.amount}"

    class Meta:
        db_table = 'payments'


class PricePlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=50)
    description = models.TextField()
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    content_rewrite = models.BooleanField(default=False, null=True, blank=True)
    seo_optimization = models.BooleanField(default=False, null=True, blank=True)
    keyword_suggestions = models.BooleanField(default=False, null=True, blank=True)
    content_automation = models.BooleanField(default=False, null=True, blank=True)
    target_audience_analysis = models.BooleanField(default=False, null=True, blank=True)
    max_posts_per_month = models.IntegerField(null=True, blank=True)

    AI_SUP = (
        ('b', 'BASIC'),
        ('i', 'INTERMEDIATE'),
        ('a', 'ADVANCED'),
        ('e', 'ENTERPRISE')
    )

    ai_support_level = models.CharField(max_length=1, choices=AI_SUP, null=True, blank=True)

    def __str__(self):
        return f"Plan ID: {self.plan_id}, Name: {self.plan_name}"

    class Meta:
        db_table = 'price_plan'


class UserPlanSubscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True, blank=True)
    plan = models.ForeignKey(PricePlan, models.DO_NOTHING, null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remaining_posts = models.IntegerField(null=True, blank=True)
    renewal_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription ID: {self.subscription_id}, User: {self.user}, Plan: {self.plan}"

    class Meta:
        db_table = 'user_plan_subscriptions'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True, max_length=100)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    # last_login = models.DateTimeField(default=datetime.datetime.now)
    role = models.CharField(max_length=5)

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}"

    class Meta:
        db_table = 'users'
