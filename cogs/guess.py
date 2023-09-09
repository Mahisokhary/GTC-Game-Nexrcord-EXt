import nextcord
import sqlite3
import random
import json

from cogs.language.guess import lang
from nextcord.ext import commands
from nextcord import slash_command

db = sqlite3.connect("gtc_guild.db")
c = db.cursor()
c.execute("""
	create table if not exists guild (
		chid integer,
		gid integer
	)
""")
db.commit()

class guess_the_country(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
	
	@slash_command(name="gtc")
	async def main(self, ctx):pass
	
	@main.subcommand(name="set-spawn", description="set which channel guess the country object spawn")
	async def set_spawn(self, ctx:nextcord.Interaction, channel:nextcord.TextChannel=None):
		if not channel:
			channel = ctx.channel
		if ctx.user.id == ctx.guild.owner_id:
			data = c.execute("select * from guild where gid=?", [ctx.guild_id]).fetchall()
			if data:
				c.execute("""
					update guild
					set chid = ?
					where gid = ?
				""", [channel.id, ctx.guild_id])
			else:
				c.execute("""
					insert into guild values (
						?, ?
					)
				""", [channel.id, ctx.guild_id])
			db.commit()
			await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("success"))
		else:
			await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("e403"))
	
	@main.subcommand(name="set-lang", description="set your language")
	async def set_lang(self, ctx:nextcord.Interaction,
		language : str = nextcord.SlashOption(
			choices={"English": "en", "Persian | فارسی":"fa"}
		)
	):
		lang(ctx.user.id, self.bot).set_lang(language)
		await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("change-lang"))
	
	@main.subcommand(name="test", description="send a experimental gtc to spawn channel")
	async def test(self, ctx:nextcord.Interaction):
		if ctx.user.id == ctx.guild.owner_id:
			data = c.execute("select * from guild where gid=?", [ctx.guild_id]).fetchall()
			if data:
				data = data[0]
				server = self.bot.get_guild(data[1])
				channel = server.get_channel(data[0])
				d = json.load(open("gtc_assets.json"))
				selected = random.choice(d)
				
				class mdl(nextcord.ui.Modal):
					def __init__(self, correct, btn, bot):
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
						else:
							await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("wrong"))
				
				class btn(nextcord.ui.View):
					def __init__(self, correct, bot):
						self.bot = bot
						super().__init__()
						self.correct = correct
					@nextcord.ui.button(label="get me!")
					async def btn(self, btn:nextcord.ui.Button, ctx:nextcord.Interaction):
						await ctx.response.send_modal(mdl(self.correct, btn, self.bot))
				
				await channel.send(file=nextcord.File(selected["asset"]), view=btn(selected["answer"][str(lang(ctx.user.id, self.bot))], self.bot))
				await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("success"))
			else:
				await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("test-eror"))
		else:
			await ctx.response.send_message(lang(ctx.user.id, self.bot).get_txt("e403"))
	
def setup(bot):
	bot.add_cog(guess_the_country(bot))
