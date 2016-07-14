from django.conf.urls import include, url
from django.views.generic import TemplateView

from .models import Strategy, TradingBot
from . import views

urlpatterns = [
    # Landing page, etc
    url(r'^$', views.landing, name="landing"),
    url(r'^faq$', TemplateView.as_view(template_name="landing/faq.html"), name="faq"),
    url(r'^pricing$', views.PlanList.as_view(), name="pricing"),
    
    # Control Panels
    url(r'^home$', views.index, name="index"),
    url(r'^strategy/([0-9]+)$', views.strategy_page, name=Strategy.EDIT_URL),
    url(r'^bot/([0-9]+)$', views.bot_page, name=TradingBot.EDIT_URL),
    url(r'^graph_data$', views.graph_data, name="graph_data"),
    
    # Legal Info
    url(r'^legal/terms$', TemplateView.as_view(template_name="main/terms.html"), name="terms"),
    url(r'^legal/privacy$', TemplateView.as_view(template_name="main/privacy.html"), name="privacy"),
    
    # API Methods
    # - CRUD for strats & bots
    url(r'^api/strategies$', views.StrategyList.as_view(), name="strategies_list"),
    url(r'^api/strategy/new$', views.StrategyNew.as_view(), name="strategy_new"),
    url(r'^api/strategy$', views.StrategyDetail.as_view(), name="strategy_detail"),
    url(r'^api/strategy/delete$', views.StrategyDelete.as_view(), name="strategy_delete"),
    
    url(r'^api/bots$', views.BotList.as_view(), name="bot_list"),
    url(r'^api/bot/new$', views.BotNew.as_view(), name="bot_new"),
    url(r'^api/bot$', views.BotDetail.as_view(), name="bot_detail"),
    url(r'^api/bot/delete$', views.BotDelete.as_view(), name="bot_delete"),
    
    # - Backtest method test
    url(r'^api/backtest$', views.BacktestDetail.as_view(), name="backtest_detail"),
]