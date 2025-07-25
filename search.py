from pyrogram import Client
from config import API_ID, API_HASH, CHANNEL_USERNAME

async def search_movie(movie_name):
    app = Client("bot_session", api_id=API_ID, api_hash=API_HASH)
    await app.start()

    results = []
    async for msg in app.search_messages(CHANNEL_USERNAME, query=movie_name):
        if msg.document:
            results.append(msg)

    await app.stop()
    return results
