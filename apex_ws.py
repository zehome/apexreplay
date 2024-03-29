#!/usr/bin/env python

# pip install aiohttp aiofiles

import aiofiles
import aiohttp
import aiopg
import asyncio
import logging
import os
import re

logger = logging.getLogger(__name__)

CONFIGPORT_RE = re.compile(r'(var|let)\s*configPort\s*=\s*([0-9]+)')
CONFIGHOST = "www.apex-timing.com"


async def wsdump(uri, name, cursor):
    logger.debug("connecting to %s", uri)
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(uri) as websocket:
            logger.debug("connected to %s", uri)
            while True:
                msg = await websocket.receive()
                frame = msg.data 
                print("<[{name}] {frame}".format(name=name, frame=frame[:16].split('\n')[0].strip()))
                if frame:
                    await cursor.execute(
                        "INSERT INTO apex_live_ws(name, frame) VALUES (%s, %s)",
                        (name, frame)
                    )

# http://www.apex-timing.com/live-timing/commonv2/javascript/javascript_live_timing.min.js
# => configHost

# http://www.apex-timing.com/live-timing/misanino-kart/javascript/config.js
# => configPort

loop = asyncio.get_event_loop()

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def timingdump(pool, track):
    url = track["url"]
    config_url = track["url"] + '/javascript/config.js'

    async with aiohttp.ClientSession() as session:
        configjs = await fetch(session, config_url)
        m = CONFIGPORT_RE.match(configjs)
        if not m:
            raise ValueError("var configPort not found in config.js")
        configport = int(m.group(2)) + 2 # apex special tricks
        wsurl = f"ws://{CONFIGHOST}:{configport}"
    logger.info(f"Loop reading websocket {wsurl}")
    while True:
        db = await pool.acquire()
        async with db.cursor() as cur:
            try:
                await wsdump(
                    uri=wsurl, name=track["name"], cursor=cur)
            except aiohttp.ClientError:
                logger.warning("websocket connection terminated. Resuming...")
            except Exception as e:
                logger.warning("websocket unknown error: %s. Resuming...", e)

async def main(dbname):
    pool = await aiopg.create_pool(database=dbname)
    db = await pool.acquire()
    async with db.cursor() as cur:
        await cur.execute("SELECT name, url FROM track")
        tracks = [{
            'name': r[0],
            'url': r[1],
        } for r in await cur.fetchall()]
    tasks = [asyncio.create_task(timingdump(pool, track)) for track in tracks]
    await asyncio.wait(tasks)

logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
loop.run_until_complete(main(dbname=os.environ["USER"]))
