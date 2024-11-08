from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters
import psutil
import time

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text('Привет!')

# Функция для получения показателей нагрузки с сетевым трафиком в процентах
async def system_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        net_io_start = psutil.net_io_counters()
        time.sleep(1)  # Ждём 1 секунду для получения скорости сети
        net_io_end = psutil.net_io_counters()

        bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
        bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv

        sent_bits_per_sec = bytes_sent * 8
        recv_bits_per_sec = bytes_recv * 8

        max_speed_bits_per_sec = 200 * 10**6  # 200 Мбит/с

        net_sent_percent = (sent_bits_per_sec / max_speed_bits_per_sec) * 100
        net_recv_percent = (recv_bits_per_sec / max_speed_bits_per_sec) * 100

        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        response = (
            f"Сервер: 89.150.59.40 (Netherlands 🇳🇱)\n"
            f"CPU: {cpu_usage}%\n"
            f"Память: {memory_usage}%\n"
            f"Нагрузка на сеть:\n"
            f"  Отправка: {net_sent_percent:.2f}%\n"
            f"  Получение: {net_recv_percent:.2f}%"
        )

        await update.message.reply_text(response)

# Основная функция, которая запускает бота
def main():
    application = Application.builder().token("").build()

    # Регистрируем обработчики с фильтром для работы в группах
    application.add_handler(CommandHandler("start", start, filters=filters.COMMAND))
    application.add_handler(CommandHandler("stats", system_stats, filters=filters.COMMAND))

    application.run_polling()

if __name__ == '__main__':
    main()
