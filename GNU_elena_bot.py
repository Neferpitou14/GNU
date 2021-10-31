import telebot
import GNU_config
import random
import json

from telebot import types

# for bot
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split

# BOT_CONFIG = GNU_config.BOT_CONFIG

# # start
# X = []
# y = []

# for intent in list(BOT_CONFIG["intents"].keys()):

#     try:

# 	    for example in BOT_CONFIG['intents'][intent]["examples"]:
# 		    X.append(example)
# 		    y.append(intent)

#     except KeyError:
#         None

# def clean(text): # очистка команды
# 	text = text.lower() # команды перевод в нижний регистр
# 	cleaned_text = ''
# 	for ch in text:
# 		if ch in 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя ': # очистка от иноязычных букв
# 			cleaned_text = cleaned_text + ch 
# 	return cleaned_text

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# vectorizer = CountVectorizer(preprocessor=clean, analyzer='char', ngram_range=(2,3))
# X_train_vect = vectorizer.fit_transform(X_train)
# X_test_vect = vectorizer.transform(X_test)

# log_reg = LogisticRegression(C=0.2)
# log_reg.fit(X_train_vect, y_train)

# print('start')

def get_intent_by_model(text):
	return log_reg.predict(vectorizer.transform([text]))[0]

def bot(question):
	intent = get_intent_by_model(question)
	return random.choice(BOT_CONFIG['intents'][intent]['responses'])

bot = telebot.TeleBot(GNU_config.TOKEN)

with open("GNU_users.json") as f:
    users = json.load(f)
with open("GNU_messags.json") as f:
    messgs = json.load(f)
with open("GNU_words.json") as f:
    words = json.load(f)

@bot.message_handler(commands=['start'])
def welcome(message):
    
    
    bot.send_message(message.chat.id, "Здравствуйте!")

    if str(message.chat.id) not in list(users.keys()):
        users.update({str(message.chat.id) : {
            "name" : None,
            "username" : message.chat.username,
            "age" : None,
            "sex" : None,
            "address" : None,
            "familiar" : False,
            "root" : False
        }})

        messgs.update({str(message.chat.id) : []})

    if users[str(message.chat.id)]["familiar"] == False:

        bot.send_message(message.chat.id, "Давайте познакомимся!\nЯ - <b>Елена</b>, и я занимаюсь улучшением условий жизни в городе Чебоксары. А как вас зовут?",
            parse_mode='html')
    

@bot.message_handler(content_types=['text'])
def lalalal(message):
    
    idi = str(message.chat.id)

    # if user is not familiar
    if users[idi]["familiar"] == False:
        if users[idi]["name"] == None:
            if message.text.split("//")[0] == "root":
                users.update({idi : {
                "name" : message.text.split("//")[1],
                "age" : None,
                "sex" : None,
                "address" : None,
                "familiar" : False,
                "root" : True
            }})
            else:
                users.update({idi : {
                    "name" : message.text,
                    "age" : None,
                    "sex" : None,
                    "address" : None,
                    "familiar" : False,
                    "root" : False
                }})

            bot.send_message(message.chat.id, "Сколько вам лет?")
        
        elif users[idi]["age"] == None:
            try:

                users.update({idi : {
                    "name" : users[idi]["name"],
                    "age" : str(int(message.text.split()[0])),
                    "sex" : None,
                    "address" : None,
                    "familiar" : False,
                    "root" : users[idi]["root"]
                }})

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Мужской", callback_data="Мужской")
                item2 = types.InlineKeyboardButton("Женский", callback_data="Женский")

                markup.add(item1, item2)

                bot.send_message(message.chat.id, "Вы молодо выглядите! Теперь немогли бы вы написать свой пол?",
                    reply_markup=markup)

            except:
                bot.send_message(message.chat.id, 'Пожалуйста, пришлите ваш возраст в виде, как в примере "<b>30 лет</b>".',
                    parse_mode='html')
        
        elif users[idi]["sex"] == None:
            if message.text == "Мужской" or message.text == "Женский":
                users.update({idi : {
                    "name" : users[idi]["name"],
                    "age" : users[idi]["age"],
                    "sex" : message.text,
                    "address" : None,
                    "familiar" : False,
                    "root" : users[idi]["root"]
                }})

                bot.send_message(message.chat.id, 'Последний этап знакомства! По какому адресу вы сейчас проживаете?')
            
            else:
                bot.send_message(message.chat.id, 'Ответьте только "Мужской" или "Женский".')
        
        else:
            users.update({idi : {
                "name" : users[idi]["name"],
                "age" : users[idi]["age"],
                "sex" : users[idi]["sex"],
                "address" : message.text,
                "familiar" : True,
                "root" : users[idi]["root"]
            }})

            bot.send_message(message.chat.id, 'Приятно познакомиться. Вместе мы построим город мечты!')

            print(message.chat.id, message.chat.username, " is new familiar")

            with open("GNU_users.json", "w") as f:
                json.dump(users, f, indent=4)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for item in words:
                item1 = types.KeyboardButton(item)
                markup.add(item1)
            
            bot.send_message(message.chat.id, 'Нам есть о чем поговорить!',
                reply_markup=markup)

    # if user tap to keyboard
    elif message.text in words and users[idi]["root"] == False:
        bot.send_message(message.chat.id, 'Пожалуста опишите проблему и на какой она улице!')
    
    # if user want root
    elif  message.text == "root":

        users.update({idi : {
                "name" : users[idi]["name"],
                "age" : users[idi]["age"],
                "sex" : users[idi]["sex"],
                "address" : message.text,
                "familiar" : True,
                "root" : True
            }})
        
    # if user not root
    elif users[idi]["root"] == False:

        bot.send_message(message.chat.id, "Хорошо")

    messg = messgs[idi]
    messg.append(message.text)
    messgs.update({idi : messg})

    with open("GNU_messags.json", "w") as f:
        json.dump(messgs, f, indent=4)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): # if user tap to inline keyboard
    try:
        if call.message:
            if call.data == "Мужской" or call.data == "Женский":
                users.update({str(call.message.chat.id) : {
                    "name" : users[str(call.message.chat.id)]["name"],
                    "age" : users[str(call.message.chat.id)]["age"],
                    "sex" : call.data,
                    "address" : None,
                    "familiar" : False,
                    "root" : users[str(call.message.chat.id)]["root"]
                }})

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Последний этап знакомства! По какому адресу вы сейчас проживаете?',
                reply_markup=None)

    except Exception as e:
        print(repr(e))

#RUN
bot.polling(none_stop=True)