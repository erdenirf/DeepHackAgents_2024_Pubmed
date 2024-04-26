
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
                'help': '/help - Get help\n/start - Call the main menu',
                'ping': 'Pong!',
                'chat': 'Send me the topic you want to find an articles on',
                'settings': 'Settings',
                'change_lang': '🌐 Choose your language',
                'change_lang_success': 'Language changed successfully!',
                'english': '🇬🇧 English',
                'russian': '🇷🇺 Russian',
                'chat_btn': '📝 Chat',
                'help_btn': '📚 Help',
                'settings_btn': '⚙️ Settings',
            }
        elif self.language == 'Ru':
            return {
                'welcome': 'Привет! Я ИИ для поиска актуальных медицинских статей по вашей теме, выберите что вы хотите сделать',
                'help': '/help - Получить помощь\n/start - Вызвать главное меню',
                'ping': 'Понг!',
                'chat': 'Напишите тему по которой хотите найти статьи',
                'settings': 'Настройки',
                'change_lang': '🌐 Выберите язык',
                'change_lang_success': 'Язык успешно изменен!',
                'english': '🇬🇧 Английский',
                'russian': '🇷🇺 Русский',
                'chat_btn': '📝 Чат',
                'help_btn': '📚 Помощь',
                'settings_btn': '⚙️ Настройки',
            }
        else:
            return {}