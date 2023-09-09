import sqlite3
import json

from nextcord.ext import commands

class UnknownTXT(Exception):
	def __str__(self):
		return "Requested txt not found"

class lang:
	def __init__(self, user_id, bot:commands.Bot):
		self.user_id = user_id
		self.bot = bot
		self.db = sqlite3.connect("lang.db")
		self.cursor = self.db.cursor()
		self.cursor.execute("""
			create table if not exists lang (
				lang varchar(255),
				disid integer
			)
		""")
		self.db.commit()
		try:
			self.lang = self.cursor.execute("select * from lang where disid=?", [self.user_id]).fetchall()[0][0]
		except IndexError:
			self.cursor.execute("insert into lang values (?, ?)", ["en", self.user_id])
			self.lang = "en"
	
	def __str__(self):
		return self.lang
	
	def set_lang(self, lang):
		self.cursor.execute("""
			update lang
			set lang = ?
			where disid = ?
		""", [lang, self.user_id])
		self.db.commit()
		self.lang = lang
	
	def get_txt(self, name) -> str:
		try:
			return json.load(open("lang.json"))[name][self.lang]
		except IndexError:
			raise UnknownTXT()
