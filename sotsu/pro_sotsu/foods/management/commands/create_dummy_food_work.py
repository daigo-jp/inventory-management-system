import random
from django.core.management.base import BaseCommand
from faker import Faker

# あなたのモデルをインポート
from foods.models import Food, WorkDatetime  # モデルの場所に合わせて修正
from home.models import StoreAccount        # StoreAccountモデルのインポート

class Command(BaseCommand):
    help = 'Create dummy data for Food and WorkDatetime models'

    def handle(self, *args, **options):
        fake = Faker('ja_JP')
        
        # --- 準備：関連するStoreAccountを取得 ---
        store_accounts = list(StoreAccount.objects.all())
        if not store_accounts:
            self.stdout.write(self.style.ERROR('No StoreAccount found. Please create StoreAccounts first.'))
            return

        # --- Foodモデルのダミーデータ作成 ---
        self.stdout.write('Creating 100 dummy food items...')
        food_categories = ['野菜', '果物', '肉類', '魚介類', '乳製品', '飲料']
        for _ in range(100):
            Food.objects.create(
                store=random.choice(store_accounts),
                name=fake.word(),
                category=random.choice(food_categories),
                cost=fake.random_int(min=100, max=2000),
                quantity=fake.random_int(min=5, max=50),
                delivery_days=fake.random_int(min=1, max=5),
                expiration_date=fake.future_date(end_date="+30d"),
                description=fake.text(max_nb_chars=100)
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 100 dummy food items.'))

        # --- WorkDatetimeモデルのダミーデータ作成 ---
        self.stdout.write('Creating 10 dummy work datetime records...')
        for _ in range(10):
            WorkDatetime.objects.create(
                store_name=fake.company(),
                work_start_time=fake.date_time_this_year(before_now=True, after_now=False),
                work_end_time=fake.date_time_this_year(before_now=False, after_now=True)
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 10 dummy work datetime records.'))