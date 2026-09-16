# Inglizcha so'zlar Telegram bot

Bot unit tanlash, inglizcha so'z berish, o'zbekcha javobni tekshirish va yakuniy natijani chiqarish uchun ishlaydi.

## Fayllar

- `main.py` — Telegram bot kodi
- `word_list.json` — 30 ta unit va so'zlar ro'yxati
- `requirements.txt` — kerakli kutubxona

## Ishga tushirish

1. `word_list.json` faylini repository ildiziga joylang.
2. Telegram'da @BotFather orqali bot token oling.
3. Kutubxonani o'rnating:

```bash
pip install -r requirements.txt
```

4. Tokenni environment variable sifatida bering:

```bash
export BOT_TOKEN="TOKENINGIZ"
python main.py
```

Windows PowerShell:

```powershell
$env:BOT_TOKEN="TOKENINGIZ"
python main.py
```

Bot `/start` buyrug'i bilan ishga tushadi. Har bir unitdan 20 tagacha savol tasodifiy tanlanadi. Bir nechta ma'no vergul, nuqtali vergul yoki `/` bilan ajratilgan bo'lsa, ulardan bittasi to'g'ri javob hisoblanadi.

**Tokenni GitHub'ga joylamang.**
