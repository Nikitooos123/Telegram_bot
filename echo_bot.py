from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType


API_TOKEN: str = '....'


# Создаем объекты бота и деспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Хендлер для комманды старт
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что нибудь')

@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

@dp.message(F.content_type == ContentType.TEXT)
async  def send_echo(message: Message):
    print(message)
    await message.answer(text=message.text)

@dp.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    print(message)
    await message.answer_photo(message.photo[0].file_id)

@dp.message(F.content_type == ContentType.AUDIO)
async def send_audio_echo(message: Message):
    print(message)
    await message.answer_audio(message.audio.file_id)

@dp.message(F.content_type == ContentType.VIDEO)
async def send_video_echo(message: Message):
    print(message)
    await message.answer_video(message.video.file_id)

@dp.message(F.content_type == ContentType.VOICE)
async def send_voice_echo(message: Message):
    print(message)
    await message.answer_voice(message.voice.file_id)

@dp.message(F.content_type == ContentType.DOCUMENT)
async def send_document_echo(message: Message):
    print(message)
    await message.answer_document(message.document.file_id)

@dp.message(F.content_type == ContentType.STICKER)
async def send_sticker_echo(message: Message):
    print(message)
    await message.answer_sticker(message.sticker.file_id)

@dp.message(F.content_type == ContentType.ANIMATION)
async def send_animation_echo(message: Message):
    print(message)
    await message.answer_animation(message.animation.file_id)

# dp.message.register(send_animation_echo, F.content_type == ContentType.ANIMATION)
# dp.message.register(send_sticker_echo, F.content_type == ContentType.STICKER)
# dp.message.register(send_document_echo, F.content_type == ContentType.DOCUMENT)
# dp.message.register(send_voice_echo, F.content_type == ContentType.VOICE)
# dp.message.register(send_video_echo, F.content_type == ContentType.VIDEO)
# dp.message.register(send_audio_echo, F.content_type == ContentType.AUDIO)
# dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
# dp.message.register(process_start_command, Command(commands=["start"]))
# dp.message.register(process_help_command, Command(commands=['help']))
# dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)