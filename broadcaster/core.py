from .adapters.medium import MediumAdapter
from .adapters.substack import SubstackAdapter

class Broadcaster:
    def __init__(self):
        self.adapters = {
            "medium": MediumAdapter(),
            "substack": SubstackAdapter()
        }

    def setup_adapter(self, platform, credentials):
        if platform not in self.adapters:
            raise ValueError(f"Platform {platform} not supported.")
        self.adapters[platform].authenticate(credentials)

    def broadcast(self, title, content, platforms=None, **kwargs):
        results = {}
        target_platforms = platforms or self.adapters.keys()

        for platform in target_platforms:
            print(f"📡 Broadcasting to {platform}...")
            try:
                adapter = self.adapters.get(platform)
                platform_kwargs = kwargs.get(platform, {})
                url = adapter.publish(title, content, **platform_kwargs)
                results[platform] = {"status": "success", "url": url}
            except Exception as e:
                results[platform] = {"status": "error", "message": str(e)}
        
        return results
