import httpx


class VASPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def check_address(self, address: str):
        url = f"{self.base_url}/api/v1/vasp/address/{address}"

        response = httpx.get(url, timeout=10.0)

        response.raise_for_status()

        return response.json()