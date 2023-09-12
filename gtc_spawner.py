import nextcord
import sqlite3
import json
import random
import asyncio
import os

from pathlib import Path
from cogs.language.guess import lang

db = sqlite3.connect("gtc_guild.db")
c = db.cursor()
c.execute("""
	create table if not exists guild (
		chid integer,
		gid integer
	)
""")
db.commit()

async def guess(bot:nextcord.ext.commands.Bot):
	while True:
		for guild in bot.guilds:
			data = c.execute("select * from guild where gid=?", [guild.id]).fetchall()
			if data:
				data = data[0]
				server = guild
				channel = server.get_channel(data[0])
				d = json.load(open("gtc_assets.json"))
				selected = random.choice([i for i in d.keys()])
				selected = d[selected]
				
				class mdl(nextcord.ui.Modal):
					def __init__(self, correct, btn, bot, selected, msg):
						self.msg = msg
						self.selected = selected
						self.bot = bot
						self.correct = correct
						self.btn = btn
						super().__init__(title="Guess The Country!")
						answer = nextcord.ui.TextInput(label="guess the country name:")
						self.add_item(answer)
						self.answer = answer
					
					async def callback(self, ctx:nextcord.Interaction):
						if self.answer.value.lower() == self.correct.lower():
							self.btn.disabled = True
							await ctx.response.send_message(ctx.user.mention + lang(ctx.user.id, self.bot).get_txt("win").format(self.correct))
							await self.msg.edit(view=None, content=f"calimed by: {ctx.user.mention}\ncorrect answer: {self.selected['answer']['en']}")
							for i in [f"users/{ctx.user.id}", f"users/{ctx.user.id}/gtc"]:
								if not Path(i).exists():
									os.system(f"mkdir {i}")
							db = sqlite3.connect(f"users/{ctx.user.id}/gtc/country.db")
							c = db.cursor()
							c.execute("""
							create table if not exists county (
								name varchar(255),
								asset varchar(255)
							)
							""")
							db.commit()
							c.execute("""
							insert into county values(?, ?)
							""", [self.selected["answer"]["en"], self.selected["asset"]])
							db.commit()
						else:
							await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("wrong"))
				
				class btn(nextcord.ui.View):
					def __init__(self, correct, bot, selected, msg):
						self.selected = selected
						self.msg = msg
						self.bot = bot
						super().__init__(timeout=60)
						self.correct = correct
					async def on_timeout(self):
						await self.msg.edit(content="timed out!", view=None)
					@nextcord.ui.button(label="Catch me!", style=nextcord.ButtonStyle.blurple)
					async def btn(self, btn:nextcord.ui.Button, ctx:nextcord.Interaction):
						await ctx.response.send_modal(mdl(self.correct, btn, self.bot, self.selected, self.msg))
				msg = await channel.send(".")
				await msg.edit(file=nextcord.File(selected["asset"]), view=btn(selected["answer"][str(lang(guild.owner_id, bot))], bot, selected, msg))
		await asyncio.sleep(1800)

def main(bot):
	asyncio.ensure_future(guess(bot))
