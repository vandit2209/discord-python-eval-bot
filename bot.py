import io
import re
import contextlib
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('You are ready to go!')


@bot.command(aliases=["eval"])
async def evaluate(ctx, *, code):
    if match := re.fullmatch(r"`(?:``(?:py(?:thon)?)?\n((?:.|\n)*)\n``|(.*))`", code):
        code = match.group(1)
        str_obj = io.StringIO()  # Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"""```
                ❌ Your code was completed with execution code 1
                {e.__class__.__name__}: {e}```""")
        return await ctx.send(f"""```
            ✅ Your code was completed with execution code 0
            {str_obj.getvalue()}```""")
    return await ctx.send('Invalid format')


bot.run("Your token here")
