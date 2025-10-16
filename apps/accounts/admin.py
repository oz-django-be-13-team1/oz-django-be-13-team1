from django.contrib import admin
from .models import Account

@admin.register(Account) # 관리자 등록
class AccountsAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "bank_code", "account_type", "balance", "created_at")
    search_fields = ("account_number", "user__username")
    list_filter = ("bank_code", "account_type")