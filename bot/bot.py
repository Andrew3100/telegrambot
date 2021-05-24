import telebot
import io
import random
from telebot import types
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

# Токен, который определяет адрес телеграм-бота
bot = telebot.TeleBot('1895961392:AAFnB2bVo9OBtZeydQupxkVMudSDzT32Oms')


# Данные для авторизации
server = 'smtp.mail.ru'
user = 'funikov.1997@mail.ru'
password = 'tiuKv2WVLdYhhlN8dSfb'


# В этот массив будем собирать поздравления
# для указанного праздника
array = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот - поздравитель. Приятно познакомиться, {message.from_user.first_name}. Я могу отправить поздравление на почту! '
                          f'праздник, с которым надо поздравить! '
                          f'Я сам придумаю текст поздравления и отправлю крутую картинку')

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        # bot.send_message(message.from_user.id, message.text)
        text = message.text
        # открываем файл с псевдонимом file.
        # !!!
        # Типы кодировок файлов:
        # Если текст русский - UTF-8 (наш случай)
        # Для английского - "windows - 1251"
        # !!!
        with io.open('сongratulations.txt', encoding='UTF-8') as file:
            # Перебор строк файла
            for line in file:
                # Если сообщение, переданное боту есть в строке
                if text in line:
                    # Из этой строки создаём массив, 1й элемент - текст поздравления
                    arr_line = line.split('. ')
                    # Текст поздравления пишем в массив
                    array.append(arr_line[1])

        # Для выбора картинки определяем в какую папку надо обратиться в
        # зависимости от типа праздника, который в переменной text
        if text == 'День рождения':
            dir_name = 'birthday'
        if text == '23 февраля':
            dir_name = 'feb23'
        if text == '8 Марта':
            dir_name = 'marth8'
        if text == 'Рождество':
            dir_name = 'christmas'
        if text == 'Новый год':
            dir_name = 'new_year'
        # имя папки
        print(dir_name)
        # Объекты письма
        recipients = ['funikov.1997@mail.ru']
        sender = 'funikov.1997@mail.ru'
        subject = 'Вам поздравление!'

        html = '<html><head></head><body style = "text-align: center"><b>' + array[
            random.randint(0, 4)] + '</b></p><body><html>'
        # В этой переменной хранится адрес картинки, отправляемой на почту
        filepath = "images/" + dir_name + "/1.png"
        # базовое имя файла
        basename = os.path.basename(filepath)
        # размер файла
        filesize = os.path.getsize(filepath)
        # может храниться как строка, так и файл любого типа
        msg = MIMEMultipart('alternative')
        # тема письма
        msg['Subject'] = subject
        # Имя отправителя, не адрес
        msg['From'] = 'Python script <' + sender + '>'
        # Присоединяем массив получателей пиьма
        msg['To'] = ', '.join(recipients)
        msg['Reply-To'] = sender
        msg['Return-Path'] = sender
        # Отправляем версию питона в заголовках
        msg['X-Mailer'] = 'Python/' + (python_version())
        # Формируем контент письма
        part_text = MIMEText(text, 'plain')
        # Указываем обработку html контента
        part_html = MIMEText(html, 'html')
        # Открываем и читаем файл с картинкой, даём имя
        part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
        part_file.set_payload(open(filepath, "rb").read())
        # Имя файла, то которое было получено при открытии
        part_file.add_header('Content-Description', basename)
        # указываем размер файла
        part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
        # Непосредственно сама отправка - указываем отправителя, получателей (можно массив, но в нашем случае )
        encoders.encode_base64(part_file)
        # добавляем все заголовки к объекту сообщения
        msg.attach(part_text)
        msg.attach(part_html)
        msg.attach(part_file)
        # соединение с SMTP, установление подключения
        mail = smtplib.SMTP_SSL(server)
        # Авторизация отправителя письма
        mail.login(user, password)
        # Сама отправка
        mail.sendmail(sender, recipients, msg.as_string())
        # Закрываем сессию SMTP, которая открыта в процессе login
        mail.quit()


bot.polling(none_stop = True)

