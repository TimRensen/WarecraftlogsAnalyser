from abc import ABC, abstractmethod

class baseWCL(ABC):
    @property
    @abstractmethod
    def authURL(self) -> str:
        pass

    @property
    @abstractmethod
    def tokenURL(self) -> str:
        pass

    @property
    @abstractmethod
    def publicURL(self) -> str:
        pass
        
    @property
    @abstractmethod
    def redirectURI(self) -> str:
        pass    
    
    @property
    @abstractmethod
    def clientID(self) -> str:
        pass

    @property
    @abstractmethod
    def clientSecret(self) -> str:
        pass
 