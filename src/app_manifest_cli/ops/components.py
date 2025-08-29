import json
from ..handlers.registry import handler

def add_component(manifest_path: str, payload_text: str, out_file):

    # Тут можно добавить логику обработки Компонент

    obj = json.loads(payload_text)
    mime = obj.get("mime-type") or obj.get("mime_type")
    handler = handler(mime)
    item = handler(obj)

    with open(manifest_path, "r", encoding="utf-8") as f:
        m = json.load(f)

    m.setdefault("components", []).append(item)
    data = json.dumps(m, ensure_ascii=False, indent=2)

    if out_file:
        out_file.write(data)
    else:
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(data)
