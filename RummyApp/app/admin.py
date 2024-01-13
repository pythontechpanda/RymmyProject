from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(State)
admin.site.register(KYCDetails)
admin.site.register(WalletAdd)
admin.site.register(WalletAmt)
admin.site.register(PayByWalletAmount)
# fsf dcas
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Hand)
admin.site.register(Game)
admin.site.register(GameRound)
admin.site.register(RoundHand)
admin.site.register(Tournaments)
admin.site.register(WithdrawRequest)
admin.site.register(Notification)
admin.site.register(HelpAndSupport)