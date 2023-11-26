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
class decllove(loader.Module):
    """If you are too humble to declare your love, use this module"""

    
    strings_ru = {
        "name": "Lover",
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
            "👋 <i>Привет. Я <b>страж очень токсичного долбаеба</b>.</i>",
            (
                "🫣 <i>Мой хозяин дурак тот ещё, и очень стесняется сказать о чем-то, поэтому он"
                " попросил меня, свое творение, помочь ему... но придется пользоваться переводчиком,порой придется переводить полностью текст, вы простите его, ведь он очень стеснителен...</i>"
            ),
            "🥰 <i>Он просто хотел, чтобы вы знали, ЧТО <b> il vous aime и сильно ценит не за внешний вид,а за ваше общение и отношение к нему, и он просил передать, что он хочет с вами проводить больше времени, ведь ему нравится проводить с вами время</b>...</i>",
            "🤗 <i>не плачьте, солнце, но если все же вы плачете, то скажите ему об этом, он постарается поддержать вас... скажу я вам одно <b> mon âme s'est épanouie comme la plus belle fleur à côté de toi.</b>merci beaucoup...</i>",
            "<i>читайте,когда тебе будет грустно и плохо.<br> ОН ЛЮБИТ ВАС И СИЛЬНО СКУЧАЕТ<br> ЕМУ НЕ ХВАТАЕТ ВАС, не хватает ваших милых разговоров, вашей милой улыбки рядом, ваших красивых глазок.<br> не хватает так же объятий теплых,которые греют не только тело, но и душу</i>",
            "❤️<i><b>хочешь расскажу как ты выглядишь в его глазах?
немного ниже его, но глаза так и манят утонуть в них , как в бескрайнем космосе, цвета немного темной грусти, но там утонул он навсегда.
волосы твои так приятны, а руки так нежны.<br> нет ничего теплее твоих объятий, нет ничего о чем он думает больше, чем о тебе.</b></i>",
            "<i>senorita, tu es belle comme le premier paysage matinal dans une nature dense, comme un chaud rayon de soleil par une journée froide et maussade.
En te voyant j'admire, j'admire ton sourire, tes yeux et ta beauté</i>",
            "🥺 <i>Это искренние чувства к вам и слова, милая леди... поэтому прошу принять это к сведению и не сильно злиться на него за его стеснительность, которую он не может побороть.</i>",
            "🫶 <i>скажу по секрету маленькому <b>tu lui manques</b> </i>",
            "🫰 <i>лучше ничего ему не говорить о нашем диалоге с вами,но не имею права вам запрещать, и если вы хотите обсудить этот диалог, то хорошо. мой совет: сказать пару ласковых словечек. ваш любимый Bl00DBot.🙂</i>",

        ],
        "talk": "🫶 поговорить",
        "404": "😢 <b>Сообщение уже исчезло. Вы не можете его прочитать...</b>",
        "read": "🫰 <b>{} брат,прости,я спалил тебя, но тебе от этого будешь лучше, я стараюсь для тебя родной мой.</b>",
        "args": (
            "<emoji document_id=6053166094816905153>💀</emoji> <b>Неверные"
            " аргументы...</b>"
        ),
    }


    async def client_ready(self):
        self.ids = self.pointer("lover", {})

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


        await message.answer(
            self.strings("ily_love")[-1],
            reply_markup=self.inline.generate_markup(
                {
                    "text": self.strings("talk"),
                    "url": f"tg://user?id={self._client.tg_id}",
                }
            ),
        )


      
