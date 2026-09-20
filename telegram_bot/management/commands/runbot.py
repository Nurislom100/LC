import asyncio
import logging

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Telegram botni ishga tushiradi (long polling)"

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
        from telegram_bot.bot import main

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            self.stdout.write("Bot to'xtatildi.")
