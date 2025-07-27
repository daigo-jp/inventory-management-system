import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

# あなたのモデルをインポート
from disposal.models import Disposal
from products.models import Product # Productモデルの場所に合わせて修正してください

User = get_user_model()

class Command(BaseCommand):
    help = 'Create dummy disposal data for the application'

    def handle(self, *args, **options):
        # --- 準備 ---
        fake = Faker('ja_JP')

        # 関連するProductとUserをDBから取得
        products = list(Product.objects.all())
        stores = list(User.objects.filter(is_staff=True)) # 例：スタッフユーザーを店舗とする

        # データが存在しない場合はエラーを出して終了
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please create products first.'))
            return
        if not stores:
            self.stdout.write(self.style.ERROR('No store users found. Please create store users first.'))
            return

        self.stdout.write('Creating dummy disposal data...')

        # --- ダミーデータを1000件作成 ---
        for _ in range(1000):
            # ランダムに商品と店舗を選ぶ
            random_product = random.choice(products)
            random_store = random.choice(stores)

            Disposal.objects.create(
                # ↓ 実際のモデルのフィールド名に合わせて修正
                disposal_menu=random_product,
                category=random_product.category,  # 商品のカテゴリをそのまま使う
                price=random_product.price,        # 商品の価格をそのまま使う
                disposal_quantity=fake.random_int(min=1, max=5),
                disposal_date=fake.date_this_year(),
                disposal_notes=fake.text(max_nb_chars=50),
                disposal_registrant=fake.name(),
                store=random_store
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully created 1000 dummy disposal data.'))