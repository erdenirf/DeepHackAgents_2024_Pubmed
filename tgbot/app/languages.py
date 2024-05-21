
class Language:
    def __init__(self, language):
        self.language = language

    def get_string(self, key):
        return self.strings.get(key, key)

    @property
    def strings(self):
        if self.language == 'Eng':
            return {
                'welcome': 'Hello! I am an AI to help you with the search of relevant medical articles on your topic, choose what you want to do',
                'help': '/menu - Call the main menu\n/start - Restart the bot',
                'ping': 'Pong!',
                'chat': 'You are now in AI chat mode! Send me the topic you want to find an articles on. To exit chat mode, type /stop',
                'settings': 'Settings',
                'change_lang': '🌐 Choose your language',
                'change_lang_success': 'Language changed successfully!',
                'english': '🇬🇧 English',
                'russian': '🇷🇺 Russian',
                'chat_btn': '📝 Chat',
                'help_btn': '📚 Help',
                'settings_btn': '⚙️ Settings',
                'chat_error': 'There was some error, please try sending your request again',
                'chat_mode_help': 'You are in chat mode, please send your request. To exit chat mode, type /stop',
                'stopped' : 'Call /menu',
                'restart' : 'There was some error, please restart the bot using /start'
            }
        elif self.language == 'Ru':
            return {
                'welcome': 'Привет! Я ИИ для поиска актуальных медицинских статей по вашей теме, выберите что вы хотите сделать',
                'help': '/menu - Вызвать главное меню\n/start - Перезапустить бота',
                'ping': 'Понг!',
                'chat': 'Вы вошли в режим ИИ чата! Напишите тему по которой хотите найти статьи. Чтобы выйти из режима чата, напишите /stop',
                'settings': 'Настройки',
                'change_lang': '🌐 Выберите язык',
                'change_lang_success': 'Язык успешно изменен!',
                'english': '🇬🇧 Английский',
                'russian': '🇷🇺 Русский',
                'chat_btn': '📝 Чат',
                'help_btn': '📚 Помощь',
                'settings_btn': '⚙️ Настройки',
                'chat_error': 'Произошла ошибка, пожалуйста, попробуйте отправить ваш запрос еще раз',
                'chat_mode_help': 'Вы в режиме чата, пожалуйста, отправьте ваш запрос. Чтобы выйти из режима чата, напишите /stop',
                'stopped' : 'Вызовите /menu',
                'restart' : 'Произошла какая-то ошибка, пожалуйста перезапустите бота используя /start'
            }
        else:
            return {}