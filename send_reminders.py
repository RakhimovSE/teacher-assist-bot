from src.telegram import TelegramClient


async def main():
    me = await client.get_me()
    print(me.stringify())


if __name__ == '__main__':
    client = TelegramClient()
    with client:
        client.loop.run_until_complete(main())
