from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Функция обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я твой бот.')

# Функция для получения показателей нагрузки с сетевым трафиком в процентах
async def system_stats(update: Update, context: CallbackContext) -> None:
    # Получение статистики
    cpu_usage = psutil.cpu_percent(interval=1)  # Загруженность CPU за 1 секунду
    memory = psutil.virtual_memory()  # Информация о памяти
    memory_usage = memory.percent  # Процент использования памяти
    net_io = psutil.net_io_counters()  # Сетевой трафик
    net_sent = net_io.bytes_sent  # Отправлено байт
    net_recv = net_io.bytes_recv  # Получено байт

    # Максимальная скорость сети в битах в секунду
    max_speed_bits_per_sec = 200 * 10**6  # 200 Мбит/с = 200 * 10^6 бит/с

    # Переводим отправленный и полученный трафик в биты и вычисляем процент от максимальной скорости
    net_sent_bits_per_sec = (net_sent * 8)  # байты в биты
    net_recv_bits_per_sec = (net_recv * 8)  # байты в биты

    net_sent_percent = (net_sent_bits_per_sec / max_speed_bits_per_sec) * 100
    net_recv_percent = (net_recv_bits_per_sec / max_speed_bits_per_sec) * 100

    # Формирование ответа
    response = (
        f"Нагрузка на CPU: {cpu_usage}%\n"
        f"Использование памяти: {memory_usage}%\n"
        f"Сетевой трафик:\n"
        f"  Отправлено: {net_sent_percent:.2f}% от максимума (200 Мбит/с)\n"
        f"  Получено: {net_recv_percent:.2f}% от максимума (200 Мбит/с)"
    )

    # Отправка сообщения
    await update.message.reply_text(response)

# Основная функция, которая запускает бота
def main():
    # Заменить YOUR_TOKEN на твой токен
    application = Application.builder().token("").build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", system_stats))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
