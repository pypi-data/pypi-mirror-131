from json import dumps, loads
from typing import Any, List, Dict

from cryptoshred.asynchronous.convenience import find_and_decrypt
from cryptoshred.backends import KeyBackend


async def decrypt_result(*, data: Any, key_backend: KeyBackend) -> List[Dict[str, Any]]:
    result = []
    for item in data:
        decrypted = await find_and_decrypt(
            x=loads(item["payload"]), key_backend=key_backend
        )
        result.append({"header": item["header"], "payload": dumps(decrypted)})
    return result
