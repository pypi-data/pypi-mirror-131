# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_broadcaster']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.11,<3.0']

setup_kwargs = {
    'name': 'aiogram-broadcaster',
    'version': '0.0.7',
    'description': 'Simple and lightweight library based on aiogram for creating telegram mailings',
    'long_description': '[![PyPI version](https://img.shields.io/pypi/v/aiogram-broadcaster.svg)](https://pypi.org/project/aiogram-broadcaster/)\n[![Python](https://img.shields.io/badge/Python-3.7+-green)](https://www.python.org/downloads/)\n[![Aiogram](https://img.shields.io/badge/aiogram-2.11+-blue)](https://pypi.org/project/aiogram/)\n[![CI](https://github.com/F0rzend/aiogram_broadcaster/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/F0rzend/aiogram_broadcaster/actions/workflows/main.yml)\n\n# Aiogram Broadcaster\n\nA simple and straightforward broadcasting implementation for aiogram\n\n## Installaiton\n\n    $ pip install aiogram-broadcaster\n\n## Examples\n\n**Few steps before getting started...**\n\n- First, you should obtain token for your bot from [BotFather](https://t.me/BotFather)\nand make sure you started a conversation with the bot.\n- Obtain your user id from [JSON Dump Bot](https://t.me/JsonDumpBot) in order to test out broadcaster.\n\n**Note:** These and even more examples can found in [`examples/`](https://github.com/fonco/aiogram_broadcaster/tree/main/examples) directory\n\n### Base usage\n```python\nfrom aiogram_broadcaster import TextBroadcaster\n\nimport asyncio\n\n\nasync def main():\n\n    # Initialize a text broadcaster (you can directly pass a token)\n    broadcaster = TextBroadcaster(\'USERS IDS HERE\', \'hello!\', bot_token=\'BOT TOKEN HERE\')\n    \n    # Run the broadcaster and close it afterwards\n    try:\n        await broadcaster.run()\n    finally:\n        await broadcaster.close_bot()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n### Embed a broadcaster in a message handler\n```python\nfrom aiogram import Bot, Dispatcher, types\n\nfrom aiogram_broadcaster import MessageBroadcaster\n\nimport asyncio\n\n\nasync def message_handler(msg: types.Message):\n    """\n    The broadcaster will flood to a user whenever it receives a message\n    """\n    \n    users = [msg.from_user.id] * 5  # Your users list\n    await MessageBroadcaster(users, msg).run()  # Run the broadcaster\n\n\nasync def main():\n\n    # Initialize a bot and a dispatcher\n    bot = Bot(token=\'BOT TOKEN HERE\')\n    dp = Dispatcher(bot=bot)\n\n    # Register a message handler\n    dp.register_message_handler(message_handler, content_types=types.ContentTypes.ANY)\n    \n    # Run the bot and close it afterwards\n    try:\n        await dp.start_polling()\n    finally:\n        await bot.session.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n',
    'author': 'F0rzend',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fonco/aiogram-broadcaster/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
