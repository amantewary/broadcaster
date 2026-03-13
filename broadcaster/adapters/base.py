from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @abstractmethod
    def authenticate(self, credentials):
        """Handle authentication for the platform."""
        pass

    @abstractmethod
    def publish(self, title, content, **kwargs):
        """Publish the content to the platform."""
        pass
