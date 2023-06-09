import subprocess

from aiofauna import ApiClient
from jinja2 import Template

from .config import env
from .repository import CodeServer, PythonContainer, User

nginx_template = Template(open("nginx.conf","r",encoding="utf-8").read())

class AuthService(ApiClient):
    """Authentication service"""
    async def authorize(self, token: str) -> User:
        data = await self.fetch(f"https://{env.OAUTH2_DOMAIN}/userinfo", headers={
            "Authorization": f"Bearer {token}"
        })
        assert isinstance(data, dict)
        return User(**data)
    
    
class CloudFlareService(ApiClient):
    """Domain provisioning service"""
    def __init__(self):
        self.headers = {
            "X-Auth-Email": env.CF_EMAIL,
            "X-Auth-Key": env.CF_API_KEY,
            "Content-Type": "application/json"
        }
        
    async def provision(self, name: str, port:int):
        """Provision a domain"""
        payload = {
            "type": "A",
            "name": name,
            "content": env.IP_ADDR,
            "ttl": 1,
            "proxied": True
        }
        response = await self.fetch(f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records", method="POST", headers=self.headers, json=payload)
        for path in ["/etc/nginx/conf.d", "/etc/nginx/sites-enabled", "/etc/nginx/sites-available"]:
            with open(f"{path}/{name}.conf","w",encoding="utf-8") as f:
                f.write(nginx_template.render(name=name,port=port))
        subprocess.run(["nginx","-s","reload"])
        return {
            "dns": response,
            "url": f"https://{name}.aiofauna.com"    
        }
        
        
            
    async def prune(self):
        records = await self.fetch(f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records", headers=self.headers)
        assert isinstance(records, dict)
        for record in records["result"]:
            await self.fetch(f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records/{record['id']}", method="DELETE", headers=self.headers)
        return {
            "message": "success"
        }
        
    async def create_worker(self, name:str, code:str):
        """Create a worker"""
        payload = {
            "name": name,
            "type": "javascript",
            "worker": code
        }
        response = await self.fetch(f"https://api.cloudflare.com/client/v4/accounts/{env.CF_ACCOUNT_ID}/workers/scripts", method="PUT", headers=self.headers, json=payload)
        return response
            
        
        
        

class DockerService(ApiClient):
    async def start_container(self, container_id:str)->None:
        await self.text(f"http://localhost:9898/containers/{container_id}/start", method="POST")
        
    async def create_volume(self, tag: str)->str:
        """Create a volume"""
        payload = {
            "Name": tag,
            "Driver": "local"
        }
        await self.fetch("http://localhost:9898/volumes/create", method="POST", headers={
            "Content-Type": "application/json"
        }, json=payload)
        return tag
        
    async def create_python_container(self, user: str, secret:str, volume:str)->PythonContainer:
        container = PythonContainer(user=user)
        payload = container.payload(secret,volume)
        response = await self.fetch("http://localhost:9898/containers/create", method="POST", headers={
            "Content-Type": "application/json"
        }, json=payload)
        assert isinstance(response, dict)
        container.container_id = response["Id"]
        instance = await container.save()
        assert isinstance(instance, PythonContainer)
        assert isinstance(instance.container_id, str)
        await self.start_container(instance.container_id)
        return instance
    
    async def create_code_server(self, user: str, secret:str, volume:str)->CodeServer:
        codeserver = CodeServer(user=user)
        payload = codeserver.payload(secret, volume)
        response = await self.fetch("http://localhost:9898/containers/create", method="POST", headers={
            "Content-Type": "application/json"
        }, json=payload)
        assert isinstance(response, dict)
        codeserver.container_id = response["Id"]
        instance = await codeserver.save()
        assert isinstance(instance, CodeServer)
        print(instance.json())
        await self.start_container(instance.container_id)
        return instance
    
    async def docker_push(self, image:str):
        """Push a docker image to the registry"""
        subprocess.run(["docker","push",image])
        
    async def get_stats(self, container_id:str):
        """Get container stats"""
        async for data in self.stream(f"http://localhost:9898/containers/{container_id}/stats", method="GET"):
            yield data
            if not data:
                break