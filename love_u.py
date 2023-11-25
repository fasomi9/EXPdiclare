# scope: hikka_only
# scope: hikka_min 1.5.3

import asyncio
import logging
import random
import time

from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import BotMessage

logger = logging.getLogger(__name__)


@loader.tds
class Declaration(loader.Module):
    """If you are too humble to declare your love, use this module"""

    strings = {
        "name": "Ksenia",
        "not_private": (
            "<emoji document_id=6053166094816905153>💀</emoji> <b>This command must be"
            " runned in personal messages...</b>"
        ),
        "ily": (
            "<emoji document_id=5465143921912846619>💭</emoji> <b>You have 1 new"
            ' message. <a href="https://t.me/{}?start=read_{}">Please, read it</a></b>'
        ),
        "ily_love": [
            "👋 <i>Hi. I'm <b>Hikka</b>.</i>",
            (
                "🫣 <i>My owner is very humble to say something, so he asked me to help"
                " him...</i>"
            ),
            "🥰 <i>He just wanted you to know, that <b>he loves you</b>...</i>",
            "🤗 <i>These are sincere feelings... Please, don't blame him.</i>",
            "🫶 <i>Better say him some warm words... 🙂</i>",
        ],
        "talk": "🫰 Talk",
        "404": "😢 <b>Message has already disappeared. You can't read it now...</b>",
        "read": "🫰 <b>{} has read your declaration</b>",
        "args": (
            "<emoji document_id=6053166094816905153>💀</emoji> <b>Wrong arguments...</b>"
        ),
    }

    strings_ru = {
        "not_private": (
            "<emoji document_id=6053166094816905153>💀</emoji> <b>Эту команду нужно"
            " выполнять в личных сообщениях...</b>"
        ),
        "ily": (
            "<emoji document_id=5465143921912846619>💭</emoji> <b>У вас 1 новое"
            ' сообщение. <a href="https://t.me/{}?start=read_{}">Пожалуйста, прочтите'
            " его</a></b>"
        ),
        "ily_love": [
            "👋 <i>Привет. Я <b>страж токсичного долбаеба</b>.</i>",
            (
                "🫣 <i>Мой хозяин дурак очень стесняется сказать о чем-то, поэтому он"
                " попросил меня помочь ему...</i>"
            ),
            "🥰 <i>Он просто хотел, чтобы вы знали, ЧТО <b>он вас любит и сильно ценит не за внешний вид,а за ваше общение и отношение к нему, и он просил передать, что он хочет с вами проводить больше времени, ведь ему нравится проводить с вами время...</b>...</i>",
            "🤗 <i>Это искренние чувства... поэтому прошу принять это к сведению и не сильно злиться на него за его стеснительность, которую он не может побороть.</i>",
            "🫶 <i>лучше ничего ему не говорить о нашем диалоге с вами. ваш любимый BloodyBot.🙂</i>",
        ],
        "talk": "💔 я сделаю вид, что не видела, слишком приторно.",
        "talk_2": "🫶 я все видела, мне очень приятно.",
        "404": "😢 <b>Сообщение уже исчезло. Вы не можете его прочитать...</b>",
        "read": "🫰 <b>{} брат,прости,я ошибся.</b>",
        "read_2": "🫰 <b>{} брат,прости,я спалил тебя, но тебе от этого будешь лучше, я стараюсь для тебя родной мой.</b>",
        "args": (
            "<emoji document_id=6053166094816905153>💀</emoji> <b>Неверные"
            " аргументы...</b>"
        ),
    }


    async def client_ready(self):
        self.ids = self.pointer("Ksenia", {})

    @loader.command(ru_doc="Признаться в любви")
    async def decl(self, message: Message):
        """Declare love"""
        if not message.is_private:
            await utils.answer(message, self.strings("not_private"))
            return

        id_ = utils.rand(8)
        await utils.answer(
            message,
            self.strings("ily").format(self.inline.bot_username, id_),
        )
        self.ids[id_] = int(time.time()) + 24 * 60 * 60

    async def aiogram_watcher(self, message: BotMessage):
        if not message.text.startswith("/start read_"):
            return

        for id_, info in self.ids.copy().items():
            if info < int(time.time()):
                self.ids.pop(id_)
                continue

        id_ = message.text.split("_")[1]
        if id_ not in self.ids:
            await message.answer(self.strings("404"))
            return

        info = self.ids.pop(id_)
        for m in self.strings("ily_love")[:-1]:
            await message.answer(m)
            await asyncio.sleep(random.randint(350, 400) / 100)

        await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("read").format(
                utils.escape_html(message.from_user.full_name),
            ),
        )
       await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("read_2").format(
                utils.escape_html(message.from_user.full_name),
            ),
        )

        await message.answer(
            self.strings("ily_love")[-1],
            reply_markup=self.inline.generate_markup(
                {
                    "text": self.strings("talk"),
                    "text_2": self.strings("talk_2"),
                    "url": f"tg://user?id={self._client.tg_id}",
                }
            ),
        )
