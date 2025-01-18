from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

# Настройка Web3 (замените на ваши данные)
infura_url = "https://github.com/delta1842/ledoviyshop.git"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Адрес вашего кошелька
shop_wallet = "YOUR_SHOP_WALLET_ADDRESS"

# Товары
products = {
    "telegram_premium": [
        {"id": 1, "name": "Telegram Premium (1 месяц)", "price_eth": 0.002},
        {"id": 2, "name": "Telegram Premium (3 месяца)", "price_eth": 0.005},
        {"id": 3, "name": "Telegram Premium (12 месяцев)", "price_eth": 0.018},
    ],
    "telegram_stars": {"id": 4, "name": "Telegram Stars", "price_per_star_eth": 0.0001},
}

# Главная страница
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Добро пожаловать в Web3-магазин Mini Apps!",
        "endpoints": {
            "GET /products": "Получить список всех товаров",
            "POST /buy": "Купить товар (укажите товар и детали в теле запроса)",
        },
    })

# Получить список всех товаров
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"products": products})

# Купить товар
@app.route("/buy", methods=["POST"])
def buy_product():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    buyer_wallet = data.get("buyer_wallet")

    # Проверка товара
    for category in products.values():
        if isinstance(category, list):
            for product in category:
                if product["id"] == product_id:
                    total_price_eth = product["price_eth"] * quantity
                    return process_payment(buyer_wallet, total_price_eth, product["name"], quantity)
        elif isinstance(category, dict) and category["id"] == product_id:
            total_price_eth = category["price_per_star_eth"] * quantity
            return process_payment(buyer_wallet, total_price_eth, category["name"], quantity)

    return jsonify({"error": "Товар с указанным ID не найден."}), 404

# Обработка платежа
def process_payment(buyer_wallet, total_price_eth, product_name, quantity):
    try:
        # Проверяем, является ли адрес покупателя валидным
        if not web3.isAddress(buyer_wallet):
            return jsonify({"error": "Неверный адрес кошелька."}), 400

        # Генерация платежных данных (информация для пользователя)
        payment_data = {
            "to": shop_wallet,
            "from": buyer_wallet,
            "value_eth": total_price_eth,
        }

        return jsonify({
            "message": f"Вы выбрали {product_name}.",
            "quantity": quantity,
            "total_price_eth": total_price_eth,
            "payment_data": payment_data,
            "instructions": f"Переведите {total_price_eth} ETH на кошелек {shop_wallet} для завершения покупки.",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
{
    "product_id": 4,
    "quantity": 100,
    "buyer_wallet": "0xYourBuyerWalletAddress"
}