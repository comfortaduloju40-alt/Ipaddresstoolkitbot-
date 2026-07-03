import httpx
from typing import Dict, Any, Optional

class BaseIPProvider:
    """Abstract Base Class providing a blueprint for IP Geolocation providers."""
    async def lookup(self, ip: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

class IPApiProvider(BaseIPProvider):
    """Production provider wrapper mapping endpoints directly to ip-api.com."""
    def __init__(self):
        # We explicitly request required metrics via query flags
        self.url = "http://ip-api.com/json/{}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,currency,mobile,proxy,hosting"

    async def lookup(self, ip: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(self.url.format(ip))
                if response.status_code != 200:
                    return None
                
                data = response.json()
                if data.get("status") == "fail":
                    return None
                return data
            except httpx.HTTPError:
                return None

# =====================================================================
# PROVIDER ROUTER CONFIGING INTERFACE
# Swap providers here (e.g., current_provider = IPInfoProvider())
# =====================================================================
current_provider = IPApiProvider()

async def get_ip_info(ip: str) -> Optional[Dict[str, Any]]:
    """Global access function executing lookup on active provider choice."""
    return await current_provider.lookup(ip)
