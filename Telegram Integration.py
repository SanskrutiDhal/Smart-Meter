from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bot")
    # Create threads for each function
    thread1 = threading.Thread(target=Alert, args=(update, context))
    thread2 = threading.Thread(target=Mesage, args=(update, context))
    thread3 = threading.Thread(target=MesageLimit, args=(update, context))
    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

def room1(update, context):
    data = ref.get()  # Retrieve data from Firebase
    category = data["Energy1"]
    response = f"Cosumption at Room 1 = {category}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
def room2(update, context):
    data = ref.get()  # Retrieve data from Firebase
    category = data["Energy2"]
    response = f"Cosumption at Room 2 = {category}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
def hub(update, context):
    data = ref.get()  # Retrieve data from Firebase
    category = data["Hub"]
    response = f"Cosumption at HUB = {category}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        
# Set up the Telegram bot
TOKEN = "6876344514:AAHzNTgS0sIkGAHxMEyODPNgvQT-WQGxDps"
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add the command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("room1", room1))
dispatcher.add_handler(CommandHandler("room2", room2))
dispatcher.add_handler(CommandHandler("hub", hub))



# Start the bot
updater.start_polling()
updater.idle()

# ... Your get_weather, is_daytime, and main functions ...

def run_weather_update():
    print("Fetching weather data...")
    main()

# Schedule the job to run every hour
schedule.every(1).seconds.do(run_weather_update)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)


measuring_thread = threading.Thread(target=measuring)
measuring_thread.start()
