# Балони — хмарна версія (GitHub). ПК щодня не потрібен.

Telegram читається безкоштовно в хмарі (GitHub Actions) раз на день.
Телефон (voice.html) сам підтягує результат за посиланням. ПК потрібен лише ОДИН раз — щоб отримати session.

## Що де лежить
- voice.html ............... голосова сторінка (її відкриває Pages)
- telegram_events.json ..... дані відвантажень (оновлює хмара)
- state.json ............... службовий (останнє оброблене повідомлення)
- cloud/fetch.py ........... хмарний зчитувач Telegram
- cloud/parser.py .......... логіка розбору
- .github/workflows/daily.yml  розклад (раз на день)
- get_session.py ........... ОДИН раз на ПК, щоб отримати session

## Налаштування (один раз, ~15 хв)
1. Створи акаунт на github.com (якщо нема).
2. New repository → назва напр. `balony` → Public → Create.
3. Завантаж усі ці файли в репозиторій (Add file → Upload files → перетягни вміст папки).
   Якщо папка `.github` не завантажилась (буває в браузері) — Add file → Create new file →
   у назві впиши `.github/workflows/daily.yml` і встав туди вміст того файлу.
4. На ПК отримай session: `pip install telethon`, потім `python get_session.py`
   (api_id/api_hash бери на https://my.telegram.org). Скопіюй надрукований рядок.
5. Репозиторій → Settings → Secrets and variables → Actions → New repository secret.
   Додай 4 секрети:
   - TG_API_ID   = твій api_id
   - TG_API_HASH = твій api_hash
   - TG_SESSION  = рядок із get_session.py
   - TG_CHAT     = Склад Гостинцеве
6. Settings → Pages → Source: Deploy from a branch → main → /(root) → Save.
   За хвилину зʼявиться адреса виду  https://ТВІЙ_НІК.github.io/balony/
7. Вкладка Actions → balony-daily → Run workflow (перевірка). Має зʼявитись/оновитись telegram_events.json.

## На телефоні
1. Відкрий  https://ТВІЙ_НІК.github.io/balony/voice.html  → меню ⋮ → Додати на головний екран.
2. ⇅ Дані → встав «Посилання на дані»:
   https://raw.githubusercontent.com/ТВІЙ_НІК/balony/main/telegram_events.json
   → 🔄 Оновити. Далі сторінка оновлюється сама при кожному відкритті.
3. ⚙️ Налаштування → впиши кульки і ціну для №1, №2.

## Щодня
Хмара сама читає Telegram. Ти лише диктуєш надходження голосом і відкриваєш сторінку —
залишок завжди свіжий. Дані публічні містять тільки тип балона / кількість / дату (без ТТН).
