from discord.ext import commands
import io
import contextlib
import re

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('You are ready to go!!')


# @commands.command(pass_context=True, hidden=True, name='eval')
# async def _eval(self, ctx, *, body: str):
#     """Evaluates a code"""
#
#     env = {
#         'bot': self.bot,
#         'ctx': ctx,
#         'channel': ctx.channel,
#         'author': ctx.author,
#         'guild': ctx.guild,
#         'message': ctx.message,
#         '_': self._last_result
#     }
#
#     env.update(globals())
#
#     body = self.cleanup_code(body)
#     stdout = io.StringIO()
#
#     to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
#
#     try:
#         exec(to_compile, env)
#     except Exception as e:
#         return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
#
#     func = env['func']
#     try:
#         with redirect_stdout(stdout):
#             ret = await func()
#     except Exception as e:
#         value = stdout.getvalue()
#         await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
#     else:
#         value = stdout.getvalue()
#         try:
#             await ctx.message.add_reaction('\u2705')
#         except:
#             pass
#
#         if ret is None:
#             if value:
#                 await ctx.send(f'```py\n{value}\n```')
#         else:
#             self._last_result = ret
#             await ctx.send(f'```py\n{value}{ret}\n```')


@bot.command()
async def eval(ctx, *, code):
    copy_code = code[:]
    pattern = re.compile(r'(`.*`)')
    reduce = pattern.finditer(code)
    index = []
    for match in reduce:
        index.extend(match.span())
    if len(index) == 2:
        code = code[index[0]:index[1]]
    elif len(index) == 4:
        code = code[index[0]:index[3]]
    print(len(code))
    print(len(copy_code))

    str_obj = io.StringIO()  # Retrieves a stream of data
    if '```python' in code:
        code = code.replace('```python', '')
    elif '```py' in code:
        code = code.replace('```py', '')
    elif '`python' in code:
        code = code.replace('`python', '')
    elif '`py' in code:
        code = code.replace('`py', '')
    elif '```' in code:
        code = code.replace('```', '', 1)
    elif '`' in code:
        code = code.replace('`', '`', 1)
    elif not index:
        return await ctx.send('```Please write inside code-blocks. Write !help for more.```')
    elif len(copy_code) != len(code):
        return await ctx.send('```Please write inside code-blocks. Write !help for more.```')

    if '```' in code:
        code = code.replace('```', '')
    else:
        code = code.replace('`', '')

    if code:
        print(code)

    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```❌ Your code was completed with execution code 1 \n{e.__class__.__name__}: {e}```")
    await ctx.send(f'```✅ Your code was completed with execution code 0 \n{str_obj.getvalue()}```')


bot.run("NzIyNDAyMTk5MjAzNzQxNzM3.XuykVA.EFwtSNvpuf7MmegA727FvZo0U-8")
