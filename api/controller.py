import asyncio
import json
from random import randint

from aiofauna import Api, EventSourceResponse, FaunaClient, q

from .config import env
from .repository import DatabaseKey, User
from .service import AuthService, CloudFlareService, DockerService

app = Api()
auth_service = AuthService()
cf_service = CloudFlareService()
fql = FaunaClient(secret=env.FAUNA_SECRET)
docker = DockerService()


async def get_database_key(user:str)->str:
    """Get the database key"""
    try:
        instance = await DatabaseKey.find_unique("user", user)
        if isinstance(instance, DatabaseKey):
            return instance.secret
        # Create a new database
        database = await fql.query(q.create_database({"name": user}))
        assert isinstance(database, dict)
        global_id = database["global_id"]
        db_ref = database["ref"]["@ref"]["id"]
        # Create a new key
        key = await fql.query(q.create_key({"database": q.database(db_ref), "role": "admin"}))
        assert isinstance(key, dict)
        key_ref = key["ref"]["@ref"]["id"]
        secret = key["secret"]
        hashed_secret = key["hashed_secret"]
        role = key["role"]
        
        await DatabaseKey(
            user=user,
            database=db_ref,
            global_id=global_id,
            key=key_ref,
            secret=secret,
            hashed_secret=hashed_secret,
            role=role
        ).save()
        
        return secret
    
    except Exception as e:
        return str(e)


@app.get("/api/auth")
async def authorize_endpoint(token:str)->User:
    """Authorize a user with a token"""
    user = await auth_service.authorize(token)
    print(user)
    response = await user.save()
    print(response)
    assert isinstance(response, User)
    return response

@app.get("/api/provision")
async def provision(name:str, port:int):
    """Provision a domain"""
    return await cf_service.provision(name, port)

@app.get("/api/pipeline")
async def pipeline(user:str):
    """Provision a domain and start a container"""
    secret = await get_database_key(user)
    volume = await docker.create_volume(user)
    python = await docker.create_python_container(user, secret, volume)
    codeserver = await docker.create_code_server(user, secret, volume)
    python_name, python_port = f"{user}-py", python.host_port
    codeserver_name, codeserver_port = user, codeserver.host_port
    python_dns = await provision(python_name, python_port)
    codeserver_dns = await provision(codeserver_name, codeserver_port)
    return {
        "python": {
            "dns": python_dns,
            "url": f"https://{python_name}.aiofauna.com"
        },
        "codeserver": {
            "dns": codeserver_dns,
            "url": f"https://{codeserver_name}.aiofauna.com"
        }
    }
    
@app.sse("/api/sse")
async def send_event(sse: EventSourceResponse):
    """Send an event"""
    await sse.send(json.dumps({"value": randint(0, 60)})) # pylint: disable=all
    await asyncio.sleep(1)
    
    
@app.sse("/api/sse/{container_id}/stats")
async def send_stats(sse: EventSourceResponse, container_id:str):
    """Send stats for a container"""
    while True:
        data = await docker.fetch("http://localhost:9898/containers/{}/stats?stream=false".format(container_id)) 
        
        assert isinstance(data, dict)
        
        cpu_delta = data['cpu_stats']['cpu_usage']['total_usage'] - data['precpu_stats']['cpu_usage']['total_usage']
        system_delta = data['cpu_stats']['system_cpu_usage'] - data['precpu_stats']['system_cpu_usage']
        cpu_percent = (cpu_delta / system_delta) * data['cpu_stats']['online_cpus'] * 100

        # Memory usage
        memory_usage = data['memory_stats']['usage']
        memory_limit = data['memory_stats']['limit']
        memory_percent = (memory_usage / memory_limit) * 100

        # Disk usage (assuming a single disk and operation type 'read' and 'write')
        disk_read = next((item['value'] for item in data['blkio_stats']['io_service_bytes_recursive'] if item['op'] == 'read'), 0)
        disk_write = next((item['value'] for item in data['blkio_stats']['io_service_bytes_recursive'] if item['op'] == 'write'), 0)

        # Network usage (assuming a single network interface 'eth0')
        network_rx = data['networks']['eth0']['rx_bytes']
        network_tx = data['networks']['eth0']['tx_bytes']

        response = json.dumps({
            "cpu": cpu_percent,
            "memory": memory_percent,
            "disk": {
                "read": disk_read,
                "write": disk_write
            },
            "network": {
                "rx": network_rx,
                "tx": network_tx
            }
        })


        await sse.send(response)
        
        await asyncio.sleep(1)
        
     

