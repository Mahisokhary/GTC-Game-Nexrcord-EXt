# GTC-Game-Nexrcord-EXt
a Guess The Country game as nextcord extension

# how to play
some country flag willl appear
in a discord channel
and to get it as reward
you should guess its name

# not complete
wait for final release...


# notice
for auto spawn add this to on_ready function:
```py
import gtc_spawner
from threading import Thread
Thread(target=gtc_spawner.main, args=[bot]).run()
```


# Languages
Persian and English

you can add more language
in:
lang.json

and define them in cogs/guess.py and cogs/language/guess.py

then translate countries name in gtc_assets.json

# County
you should add countries by your self
add picture to any folder

and define it in gtc_assets.json
