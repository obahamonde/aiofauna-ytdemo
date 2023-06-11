from typing import Any, Dict, List, Optional

from aiofauna import FaunaModel, Field

from .utils import gen_port


class User(FaunaModel):
    """OAuth2 user"""

    email: Optional[str] = Field(default=None, index=True)
    email_verified: Optional[bool] = Field(default=False)
    family_name: Optional[str] = Field(default=None)
    given_name: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    sub: str = Field(..., unique=True)
    updated_at: Optional[str] = Field(default=None)
    
class DatabaseKey(FaunaModel):
    user:str = Field(..., unique=True)
    database: str = Field(...)
    global_id: str = Field(...)
    key: str = Field(...)
    secret: str = Field(...)
    hashed_secret: str = Field(...)
    role: str = Field(...)


class CodeServer(FaunaModel):
    container_id: Optional[str] = Field(default=None, unique=True)
    user: str = Field(..., description="User reference", unique=True)
    image: str = Field(default="code-server", description="Image to use")
    host_port: int = Field(default_factory=gen_port, description="Port to expose")
    env_vars: Optional[List[str]] = Field(default=[], description="Environment variables")

    def payload(self, secret: str, volume:str) -> Dict[str, Any]:
        assert isinstance(self.env_vars, list)
        self.env_vars.append(f"FAUNA_SECRET={secret}")
        self.env_vars.append(f"PASSWORD={self.user}")
        self.env_vars.append("TZ=America/New_York")
        self.env_vars.append(f"PUID={self.user}")
        self.env_vars.append(f"PGID={self.user}")
        self.env_vars.append(f"USER={self.user}")
        self.env_vars.append(f"SUDO_PASSWORD={self.user}")
        return {
            "Image": self.image,
            "Env": self.env_vars,
            "ExposedPorts": {
                "8443/tcp": {
                    "HostPort": str(self.host_port)
                }
            },
            "HostConfig": {
                "PortBindings": {
                    "8443/tcp": [
                        {"HostPort": str(self.host_port)}
                    ]
                },
                "Binds": [f"{volume}:/config/workspace"]
            }
        }
    
class PythonContainer(FaunaModel):
    """AioFauna container"""
    container_id: Optional[str] = Field(default=None, unique=True)
    user: str = Field(..., description="User reference", unique=True)
    image: str = Field(default="python-dev", description="Image to use")
    host_port: int = Field(default_factory=gen_port, description="Port to expose")
    container_port: int = Field(default=8080, description="Port to expose")
    env_vars: Optional[List[str]] = Field(default=[], description="Environment variables")
   
 
    def payload(self, secret: str, volume:str) -> Dict[str, Any]:  
        assert isinstance(self.env_vars, list)
        self.env_vars.append(f"FAUNA_SECRET={secret}")
        return {
            "Image": self.image,
            "Env": self.env_vars,
            "ExposedPorts": {
                f"{self.container_port}/tcp": {},
            },
            "HostConfig": {
                "PortBindings": {
                    f"{self.container_port}/tcp": [
                        {"HostPort": str(self.host_port)}
                    ]
                },
                "Binds": [f"{volume}:/app"]
            }
        }
    