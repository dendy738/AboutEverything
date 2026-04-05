import asyncio
import aiohttp

CENSURED_API = 'wCpJ8W67bJCBFUHXzri5H4UZc2DAht4jB0ovxyRe'


async def check_for_profanity(text):
    base_url = f'https://api.api-ninjas.com/v1/profanityfilter?text={text}'
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, headers={'X-Api-Key': CENSURED_API}) as response:
            result = await response.json()
            return result.get('has_profanity')


async def main_check_profanity(title, description=None):
    if description is None:
        return await check_for_profanity(title)
    else:
        results = await asyncio.gather(check_for_profanity(title), check_for_profanity(description))
        return any(results)

