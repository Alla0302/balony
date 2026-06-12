"""
fetch.py — запускається в GitHub Actions раз на день.
Читає нові повідомлення чату складу, розбирає (parser.py) і дописує
telegram_events.json + state.json у корінь репозиторію. Excel тут не потрібен.
Ключі беруться з GitHub Secrets (env), у коді нічого не зберігається.
"""
import os, json
from parser import parse_stream

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVENTS = os.path.join(ROOT, "telegram_events.json")
STATE = os.path.join(ROOT, "state.json")


def load(p, d):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return d


def iso(x):
    return x.date().isoformat() if hasattr(x, "date") else str(x)


def main():
    api_id = int(os.environ["TG_API_ID"])
    api_hash = os.environ["TG_API_HASH"]
    session = os.environ["TG_SESSION"]
    chat = os.environ["TG_CHAT"]

    state = load(STATE, {"last_id": 0})
    last = state.get("last_id", 0)

    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    msgs = []
    with TelegramClient(StringSession(session), api_id, api_hash) as client:
        try:
            entity = client.get_entity(int(chat))
        except (ValueError, TypeError):
            entity = client.get_entity(chat)
        for m in client.iter_messages(entity, min_id=last):
            if m.message:
                msgs.append({"id": m.id, "date": m.date, "text": m.message})
    msgs.sort(key=lambda x: x["id"])
    if not msgs:
        print("Нових повідомлень немає.")
        return

    events = parse_stream(msgs)
    existing = load(EVENTS, [])
    have = {e.get("id") for e in existing}
    added = 0
    for i, e in enumerate(events):
        eid = f"t{e['msg_id']}_{e['ttn'] or i}"
        if eid in have:
            continue
        existing.append({"id": eid, "date": iso(e["date"]),
                         "balon": e["balon"], "type": e["type"], "qty": e["qty"]})
        have.add(eid)
        added += 1
    json.dump(existing, open(EVENTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    state["last_id"] = max(m["id"] for m in msgs)
    json.dump(state, open(STATE, "w", encoding="utf-8"))
    print(f"Опрацьовано {len(msgs)} повідомлень, додано {added} подій.")


if __name__ == "__main__":
    main()
