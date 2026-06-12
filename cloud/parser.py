"""
parser.py — розбір повідомлень чату «Склад Гостинцеве» у події складу.

Логіка (твоя):
  • «Номер X» (X=1..6) задає активний тип балона для наступних ТТН
  • 14-значний номер у повідомленні = одна Відправка активного типу
  • «дві штуки в одну відправку» / «2 шт» → кількість 2
    (працює і коли фраза йде окремим повідомленням одразу після ТТН)
  • «повернути / переадресувати / не відправляй» → Повернення (повертає балон на склад)

parse_stream() — чиста функція без залежностей, її легко тестувати.
"""
import re

TTN_RE = re.compile(r'(?<!\d)(\d{14})(?!\d)')
NUM_RE = re.compile(r'номер\s*0*([1-6])', re.IGNORECASE)
RET_RE = re.compile(r'поверн|переадрес|не\s*відправл|не\s*отправл|не\s*везд', re.IGNORECASE)
X2_RE  = re.compile(r'дв[іе]\s*штук|2\s*штук|2\s*шт|дв[іе]\s*в\s*одну', re.IGNORECASE)


def _find_ttns(text):
    found = TTN_RE.findall(text)
    if not found:                      # запасний варіант: ТТН вставлено з пробілами
        found = TTN_RE.findall(re.sub(r'(?<=\d)[ \u00a0](?=\d)', '', text))
    return found


def parse_stream(messages):
    """
    messages: список dict {id, date, text}, відсортований за часом (старі → нові).
    Повертає список подій: {date, balon, type, qty, ttn, msg_id}.
    """
    active = None
    events = []
    last_ship = None
    for m in messages:
        text = (m.get('text') or '').strip()
        if not text:
            continue
        nm = NUM_RE.search(text)
        if nm:
            active = nm.group(1)
        ttns = _find_ttns(text)
        is_ret = bool(RET_RE.search(text))
        is_x2 = bool(X2_RE.search(text))
        if ttns:
            for ttn in ttns:
                ev = {'date': m.get('date'), 'balon': active,
                      'type': 'Повернення' if is_ret else 'Відправка',
                      'qty': 2 if is_x2 else 1, 'ttn': ttn, 'msg_id': m.get('id')}
                events.append(ev)
                last_ship = ev
        else:
            if is_ret and active:
                ev = {'date': m.get('date'), 'balon': active, 'type': 'Повернення',
                      'qty': 1, 'ttn': '', 'msg_id': m.get('id')}
                events.append(ev)
                last_ship = ev
            elif is_x2 and last_ship is not None and last_ship['type'] == 'Відправка':
                last_ship['qty'] = 2     # фраза «дві штуки» окремим повідомленням
    return events
