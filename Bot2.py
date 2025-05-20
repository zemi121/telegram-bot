import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import time
import threading

# 🔑 Vlož svůj vlastní TOKEN od BotFather
TOKEN = '8186499686:AAEvvBzw1qQbxvf-lnXopxWC_sIV1sgFdiI'

# 📋 Otázky a odpovědi
questions = [
    {"text": "V 51 letech zemřel historicky nejvýznamnější vůdce Francie. Na jeho jméno se ptát nepotřebuji, to by bylo příliš snadné. Mě by spíše zajímalo – na jakém ostrůvku si naposledy říkal, že dovolená v exotice vlastně není zas taková výhra?", "answer": "svatá helena"},
    {"text": "21. května 1955 vydal jeden z průkopníků roke and rollu svůj první singl. Jak se jmenuje slavná píseň od Chucka Berryho?", "answer": "maybellene"},
    {"text": "Když jsi slavila 16 narozeniny, lidé v USA stáli dlouhé fronty do kina na druhý díl filmové ságy o hvězdných válkách. Jak se celá série nazývá?", "answer": "star wars"},
    {"text": "21. května 1927 se jeden dobrodruh vydal přes oceán. Nepotřeboval posádku, GPS ani Spotify. Vystartoval z New Yorku a skončil v Paříži – bez mezipřistání – jako první v historii. Jak se jmenoval jeho slavný ocelový letoun? (celý anglický název bez zkratek)", "answer": "spirit of saint louis"},
    {"text": "21. května přišel velký den pro zdraví všech američanů. Clara Barton založila neziskovou organizaci, která poskytovala své služby například po potopení RMS Titanic. Jaký je její 3slovný název v angličtině?", "answer": "american red cross"},
    {"text": "V květnu roku 1956 se zpívalo poprvé, ale ne naposled. Vítěz si sice odnesl trofej, ale i tak mu doma nerozuměli. Jak se jmenuje soutěž, kde téměř každý rok Skandinávie zahanbí všechny kromě Ukrajiny? (anglický název)", "answer": "eurovision"},
    {"text": "Charles Lindbergh ale nebyl jediný letec, který se nesmazatelně podepsal pod den 21. května. O stejný čin, jako on se o 5 let později pokusila i první žena, které se to povedlo. Jaké je její celé jméno? ", "answer": "amelia earhart"},
    {"text": "21. května 2001 jsme poprvé v kinech zjistili, že i zlobři mají city. V kině jsme se poprvé setkali s oslem, který nezavřel pusu. Jak se jmenoval film i hlavní postava?", "answer": "shrek"},
    {"text": "Říkalo se jim „plážoví kluci“, ale tahle deska byla všechno, jen ne povrchní. V květnu 1966 vyšlo album, které rozbrečelo i Beatles. Jaký je jeho název?", "answer": "pet sounds"},
    {"text": "Během tvých 34. narozenin přistávala na jedné nedaleké planetě sonda, které potvrdila přítomnost vody ve Vesmíru i mimo Zemi. Jak se sonda jmenovala? (Snad je jen náhoda, že její činnost skončila kolem 4. narozenin tvé dcery)", "answer": "phoenix"},
    {"text": "Velký den pro hráče přišel 21. května 2013, kdy Microsoft uvedl na trh svoji novou konzoli. Jaké je její celé jméno?", "answer": "xbox one"},
    {"text": "Sestav tajemku", "answer": "ty stará kuno"},  # Tuhle upravíš později
    {"text": "Zde vložte text", "answer": ""}  # Zpráva 13
]

user_states = {}

# ⚙️ Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text("Ahoj, vítej ve své narozeninové hře. Mysli na to, že si píšeš s narychlo připraveným robotem, takže se můžeme jen společně modlit, že dojdeme do kýženého cíle. Čeká tě pár otázek, díky kterým se snad o dnešku a o věku 51 let něco dozvíš. Odpovídej vždy pouze na otázku, bez dalších slov. Můžeš zkoušet různé varianty a pokud nic nepomůže, tak to ještě zkus napsat malým písmem bez diakritiky, pokud ani to nepomůže, pak to nejspíše není správná odpověď. A teď už jdeme na to!")
    user_states[user_id] = {"current_question": 0, "timer": None}
    threading.Timer(40.0, send_question, args=(update, context, user_id)).start()

def send_question(update, context, user_id):
    q_index = user_states[user_id]["current_question"]
    if q_index < len(questions):
        context.bot.send_message(chat_id=user_id, text=questions[q_index]["text"])

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text.lower().strip()

    if user_id not in user_states:
        update.message.reply_text("Napiš /start pro spuštění hry.")
        return

    state = user_states[user_id]
    q_index = state["current_question"]
    correct_answer = questions[q_index]["answer"].lower()

    if user_text == correct_answer:
        update.message.reply_text("Správně! Ale očekávej pokračování!")
        state["current_question"] += 1

        # Pokud jsme u otázky 11 -> hned pošleme otázku 12
        if q_index == 10:
            send_question(update, context, user_id)

        # Pokud jsme u otázky 12 -> hned pošleme otázku 13
        elif q_index == 11:
            send_question(update, context, user_id)

        # Pokud jsme na konci, nedělej nic
        elif state["current_question"] >= len(questions):
            return

        else:
            # U všech ostatních počkej 30 minut
            def delayed_question():
                send_question(update, context, user_id)
            timer = threading.Timer(18, delayed_question)
            timer.start()
            state["timer"] = timer
    else:
        update.message.reply_text("Toto není správná odpověď.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()