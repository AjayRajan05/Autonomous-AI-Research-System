from typing import Any, Dict


class SessionMemory:
    """
    Shared runtime memory across agents in a pipeline execution.
    """

    def __init__(self):
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._store[key] = value

    def get(self, key: str, default=None):
        return self._store.get(key, default)

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._store)


if __name__ == "__main__":
    mem = SessionMemory()
    mem.set("query", "transformers in healthcare")
    print(mem.snapshot())