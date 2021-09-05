import asyncio
from typing import Dict, List, Tuple

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from service.core.config import PROJECT_NAME, RESPONSE_TEMPLATE, WORDS_URL

app = FastAPI(
    title=PROJECT_NAME
)


@app.get("/ping", summary="Check that the service is operational")
async def pong():
    """
    Sanity check - this will let the user know that the service is operational.
    It is also used as part of the HEALTHCHECK.
    Docker uses curl to check that the API service is still running, by exercising this endpoint.
    """
    return {"ping": "pong!"}


async def perform_request(client: httpx.AsyncClient, word: str) -> Tuple[str, str]:
    """
    Performs request to external API
    """
    response = await client.get(word)
    return word, response.json()


async def gather_tasks(words: List[str]) -> Dict[str, str]:
    """
    Gathers words to request them asynchronously from external API
    """
    async with httpx.AsyncClient(base_url=WORDS_URL) as async_client:
        tasks = [perform_request(async_client, word) for word in words]
        result = await asyncio.gather(*tasks)
        return dict(result)


@app.get('/madlib', summary='Returns templated "madlib" sentence')
async def madlib_endpoint():
    """
    Returns templated "madlib" sentence getting components from external API
    """
    words = await gather_tasks(['adjective', 'verb', 'noun'])
    result = RESPONSE_TEMPLATE.format(**words)
    return result


@app.get('/', response_class=HTMLResponse, summary='Links to docs and madlib')
async def root():
    return """
    <html>
        <head>
            <title>madlib</title>
        </head>
        <body>
            <h1>madlib</h1>
            <ul>
                <li><a href='/docs'>docs</a></li>
                <li><a href='/madlib'>madlib</a></li>
            </ul>
        </body>
    </html>
    """
