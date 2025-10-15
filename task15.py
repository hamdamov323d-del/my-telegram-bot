import requests
import json
import logging

# Танзимоти асосӣ
BOT_TOKEN = "8386206695:AAHUkWgB50ouq_FoVVet3AsDIH-XlxtAYNw"
YOUR_CHAT_ID = "+79241626391"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_bot_connection():
    """Санҷиши пайвастшавӣ бо Telegram API"""
    print("🔍 Санҷиши пайвастшавӣ...")
    
    # 1. Санҷиши Token
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Token дуруст аст")
            print(f"🤖 Бот: {bot_info['first_name']} (@{bot_info['username']})")
            print(f"🆔 ID бот: {bot_info['id']}")
        else:
            print(f"❌ Token нодуруст: {data.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Хато дар пайвастшавӣ: {e}")
        return False
    
    # 2. Санҷиши Chat ID
    print(f"\n🔍 Санҷиши Chat ID: {YOUR_CHAT_ID}")
    test_message = "✅ Санҷиши пайвастшавӣ. Ин бот кор мекунад!"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": test_message
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            print("✅ Паём ба шумо фиристода шуд!")
            print(f"📨 ID паём: {data['result']['message_id']}")
        else:
            print(f"❌ Хато дар фиристодани паём: {data.get('description')}")
            print("❌ Эҳтимол Chat ID нодуруст аст!")
            
    except Exception as e:
        print(f"❌ Хато: {e}")
    
    return True

def get_all_updates():
    """Гирифтани ҳамаи паёмҳои охирин"""
    print(f"\n📨 Гирифтани ҳамаи паёмҳо...")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            updates = data['result']
            if updates:
                print(f"✅ {len(updates)} паём ёфт шуд:")
                print("-" * 50)
                
                for i, update in enumerate(updates, 1):
                    message = update.get('message', {})
                    user = message.get('from', {})
                    chat = message.get('chat', {})
                    
                    print(f"\n📝 Паём #{i}:")
                    print(f"   🆔 Update ID: {update['update_id']}")
                    print(f"   👤 Корбар: {user.get('first_name', 'Номаълум')}")
                    print(f"   📱 Username: @{user.get('username', 'Номаълум')}")
                    print(f"   🆔 User ID: {user.get('id', 'Номаълум')}")
                    print(f"   💬 Матн: {message.get('text', 'Номаълум')}")
                    print(f"   🆔 Chat ID: {chat.get('id', 'Номаълум')}")
                    print(f"   ⏰ Вақт: {message.get('date', 'Номаълум')}")
                    print("-" * 30)
            else:
                print("❌ Ягон паём нест. Ба бот паём фиристед!")
        else:
            print(f"❌ Хато: {data.get('description')}")
            
    except Exception as e:
        print(f"❌ Хато дар гирифтани паёмҳо: {e}")

def simple_bot():
    """Боти хеле содда барои санҷиш"""
    print(f"\n🤖 Оғози боти санҷишӣ...")
    print("📱 Ба бот равед ва /start-ро фиристед")
    
    last_update_id = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 30}
            
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        last_update_id = update['update_id']
                        message = update.get('message', {})
                        text = message.get('text', '')
                        user = message.get('from', {})
                        chat = message.get('chat', {})
                        
                        if text == '/start':
                            print(f"\n🎉 КОРБАР ОМАД!")
                            print(f"👤 Ном: {user.get('first_name', 'Номаълум')}")
                            print(f"📱 Username: @{user.get('username', 'Номаълум')}")
                            print(f"🆔 User ID: {user.get('id')}")
                            print(f"💬 Chat ID: {chat.get('id')}")
                            
                            # Маълумот ба администратор
                            admin_message = f"""
🎉 КОРБАР БОТРО ОҒОЗ КАРД!

👤 Ном: {user.get('first_name', 'Номаълум')}
📱 Username: @{user.get('username', 'Номаълум')}
🆔 User ID: {user.get('id')}
💬 Chat ID: {chat.get('id')}
⏰ Вақт: {message.get('date')}
                            """
                            
                            # Фиристодани маълумот ба шумо
                            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                            requests.post(send_url, json={
                                "chat_id": YOUR_CHAT_ID,
                                "text": admin_message
                            })
                            
                            # Покуҳиш ба корбар
                            requests.post(send_url, json={
                                "chat_id": chat['id'],
                                "text": f"Салом {user.get('first_name')}! ✅ Маълумот ба администратор фиристода шуд."
                            })
            
            # Интизорӣ
            import time
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n⏹ Бот қатъ карда шуд")
            break
        except Exception as e:
            print(f"❌ Хато: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 САНҶИШИ БОТИ TELEGRAM")
    print("=" * 60)
    
    # Санҷиши пайвастшавӣ
    if test_bot_connection():
        # Гирифтани паёмҳои мавҷуд
        get_all_updates()
        
        # Оғози бот
        simple_bot()
    else:
        print("\n❌ Лутфан Token-и дурустро ворид кунед!")