# cb-i18n

Advanced internationalisation (i18n) support for Discord bots

This module works with any well-known Discord API library for Python, including:

- [discord.py](https://github.com/Rapptz/discord.py) (and any derived libraries such as [disnake](https://github.com/DisnakeDev/disnake), [nextcord](https://github.com/nextcord/nextcord) and [pycord](https://github.com/Pycord-Development/pycord))
- [hikari.py](https://github.com/hikari-py/hikari)

### Installation

Install with pip:

```sh
# Linux / MacOS
python3 -m pip install cb-i18n

# Windows
py -3 -m pip install cb-i18n
```

Install from source:

```sh
git clone https://github.com/LTT/cb-i18n
cd cb-i18n
python3 setup.py install

# Windows
git clone https://github.com/LTT/cb-i18n
cd cb-i18n
py -3 setup.py install
```

### Example usage of `cb-i18n`:

*In fact, this library can work with just any application written in python. The first arg in `Translator.translate` can be **anything**, you can pass integer, string, custom object or even module, all will work as expected by you. Internally, lib does nothing with that "context", it just passing it to your `locale_getter` and all.*

Directory structure:

```
src/
  languages/
    en-US.json
    ru-RU.json
  main.py
```

`src/languages/en-US.json`:
```json
{
  "Hello {}": "Hello {}", // Positional placeholders
  "You're a Genius!": "You're a Genius!", // No placeholders
  "Locale is now {locale}": "Locale is now {locale}" // Keyword-only placeholders
}
```

`src/languages/ru-RU.json`:
```json
{
  "Hello {}": "Привет {}",
  "You're a Genius!": "Да ты гений!",
  "Locale is now {locale}": "Язык теперь {locale}"
}
```

`src/main.py`:
```py
import sqlite3
import disnake
from disnake.ext import commands
import cb_i18n as i18n

bot = commands.Bot("!", intents=disnake.Intents.all())

connection = sqlite3.connect('mydatabase.db')
cursor = connection.cursor()

translator = None
_ = None

def get_locale(ctx: commands.Context):
    return cursor.execute("SELECT locale FROM guilds WHERE id = ?;", ctx.guild.id).fetchone()[0]

@bot.event
async def on_ready():
    print("Bot loading")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS guilds (id bigint, locale text);")
    connection.commit()
    
    print("  Loading guilds table...")
    for guild in bot.guilds:
        if not cursor.execute("SELECT * FROM guilds WHERE id = ?", guild.id).fetchone():
            print("    Guild {}: not exist".format(guild.id))
            
            cursor.execute("INSERT INTO guilds VALUES (?, ?);", guild.id, "en-US")
            connection.commit()
        else:
            print("    Guild {}: exists".format(guild.id))
    print("  Loaded guilds table.")
    
    print("  Loading i18n...")
    global translator, _
    
    translator = i18n.make_translator()
    translator.set_locale_dir("./languages/")
    translator.set_locale_getter(get_locale)
    translator.load_translations()
    _ = translator.translate
    print("  Loaded i18n.")
    
    print("Bot ready!\nAccount: {} (ID: {})\nGuild count: {}\nUser count: {}".format(str(bot.user), bot.user.id, len(bot.guilds), len(bot.users)))

@bot.command(description="Set locale for a guild", aliases=["setlocale", "set-locale"])
async def set_locale(ctx: commands.Context, locale: str):
    cursor.execute("UPDATE guilds SET locale = ? WHERE id = ?;", locale, ctx.guild.id)
    connection.commit()
    
    return await ctx.send(_(ctx, "Locale is now {locale}").format(locale=locale))

@bot.command(description="Say hi!")
async def hi(ctx: commands.Context, name: str):
    return await ctx.send(_(ctx, "Hello {}").format(name))

@bot.command(description="You're Genius, right?")
async def genius(ctx: commands.Context):
    return await ctx.send(_(ctx, "You're a Genius!"))

try:
    bot.run(os.environ.get("BOT_TOKEN"))
except Exception as exc:
    print(exc.__class__.__name__ + ": " + exc.__str__() + "".join(tb.format_exception(exc)))
finally:
    cursor.close()
    connection.close()
```
