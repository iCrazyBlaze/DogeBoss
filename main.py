import asyncio
import datetime
import inspect
import json
import locale
import os
import random
import re
import string
import time
from datetime import datetime

import aiohttp
import dogehouse
import requests
from bs4 import BeautifulSoup
from covid import Covid
from dogehouse import DogeClient, command, event
from dogehouse.entities import Message, User

from keep_alive import keep_alive

# Set this to true if running on repl.it, to keep the process alive
run_on_repl = False

DOGETOKEN = os.getenv('DOGEHOUSE_TOKEN')
DOGEREFRESHTOKEN = os.getenv('DOGEHOUSE_REFRESH_TOKEN')

launch_time = datetime.utcnow()
locale.setlocale( locale.LC_ALL, '' )

class Client(DogeClient):
    @event
    async def on_ready(self):
        print(f"Successfully connected as {self.user}!")
        await self.create_room("DogeBoss!")
        await self.send(f"Hey! My name is DogeBoss! I'm a multi-purpose chatbot, to see my features, type:ㅤㅤ {self.prefix}help")

    # Events, Starboard right here;

    @event
    async def on_message(self, message: Message):
        if message.content.startswith(self.prefix):
            pass
        elif message.content.startswith("!"):
            pass
        elif message.content.startswith("."):
            pass
        elif message.content.startswith("h!"):
            pass  # code above made sure that the starred message wouldn't be a bot message
        else:
            global msg  # making the two variables global so we can use them across the whole file
            global msgauthor
            msg = message.content
            msgauthor = message.author.username

    @command
    async def setstar(self, ctx: Message):
        """Sets a message to be 'starred'. The current starred message can be accessed using the 'starred' command."""
        global msg
        global msgauthor
        global starred  # also making those global so we can use them across the whole file
        global starredauthor
        starred = msg
        starredauthor = msgauthor
        await self.send(f"Starred message was set!")

    @command
    async def starred(self, ctx: Message):
        """Reads the current starred message"""
        global starred
        global starredauthor
        await self.send(f"Starred Message: {starred}ㅤ|ㅤMessage Creator: @{starredauthor}")

    @command
    async def whoami(self, ctx: Message):
        """Gets info about yourself"""
        await self.userinfo(self, ctx)

    @command
    async def whereami(self, ctx: Message):
        """Gets info about the room you're in"""
        await self.send(f"Name: {self.room.name} • Description: {self.room.description} • ID: {self.room.id} • Member Count: {self.room.count} • Created at: {self.room.created_at} • Is Private?: {self.room.is_private}")

    @command
    async def slots(self, ctx: Message):
        """Plays a slot machine"""

        final = []
        for i in range(5):
            a = random.choice([":redDogeHouse:", ":OrangeDogeHouse:", ":PurpleDogeHouse:", ":CyanDogeHouse:", ":CoolHouse:"])

            final.append(a)


        final_set = set(final)

        # Checks if they are all the same
        if len(final_set) == 1:
            return await self.send(f"{ctx.author.mention} Triple! You won!ㅤ •ㅤ {' | '.join(final)}")
        # Checks if at least 2 are the same
        elif len(final) != len(final_set):
            return await self.send(f"{ctx.author.mention} You won!ㅤ •ㅤ {' | '.join(final)}")
        else:
            return await self.send(f"{ctx.author.mention} You lost!ㅤ •ㅤ {' | '.join(final)}")

    @command
    async def crypto(self, ctx: Message, currency: str):
        """Returns stats for the specified cryptocurrency :CryptoDOGE:"""
        
        # Get the current currency symbol name to get the right price for that currency
        curr_symbol = locale.localeconv()['int_curr_symbol'].lower()

        req = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={curr_symbol}&ids={currency}").json()
        if req == []:
            return await self.send(f"I couldn't find any results for the cryptocurrency: {currency} • Example: {self.prefix}crypto bitcoin")
        rejson = req[0]

        name = rejson["name"]
        symbol = rejson["symbol"].upper()
        price = locale.currency(rejson["current_price"]) # Format as currency
        ranked = rejson["market_cap_rank"]
        twenty_high = rejson["high_24h"]
        twenty_low = rejson["low_24h"]
        twenty_change = rejson["price_change_24h"]
        twenty_perc = rejson["price_change_percentage_24h"]
        updated = rejson["last_updated"]
        ath = rejson["ath"]
        ath_change_perc = rejson["ath_change_percentage"]
        ath_date1 = rejson["ath_date"]
        ath_date = ath_date1[:-14]
        atl = rejson["atl"]
        atl_change_perc = rejson["atl_change_percentage"]
        atl_date1 = rejson["atl_date"]
        atl_date = atl_date1[:-14]
        lupdt = updated[:-14]

        # just for the ranked 2 last characters
        if ranked == 1:
            rankedsym = "st"
        elif ranked == 2:
            rankedsym = "nd"
        elif ranked == 3:
            rankedsym = "rd"
        else:
            rankedsym = "th"

        await self.send(f"Crypto data for: {name} ({symbol}) • Current Price: {price} • Ranked: {ranked}{rankedsym} • Last 24h stats: Highest: {twenty_high}, Lowest: {twenty_low}, Change: {twenty_change}, Change in %: {twenty_perc}% • All Time High (ATH): {ath}, ATH Change in %: {ath_change_perc}%, ATH at: {ath_date} • All Time Low (ATL): {atl}, ATL Change in %: {atl_change_perc}%, ATL at: {atl_date} • Last update at {lupdt}")

    # RonaRage/iCrazyBlaze
    @command
    async def dog(self, ctx: Message):
        """Returns a random image of a dog"""
        image_url = requests.get("https://api.thedogapi.com/v1/images/search", headers={"x-api-key": "d0558cf8-f941-42f7-8daa-6741a67c5a2e"}).json()[0]["url"]
        await self.send(image_url)

    @command
    async def cat(self, ctx: Message):
        """Returns a random image of a cat"""
        image_url = requests.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": "37b77c23-9000-46c8-b808-a224a26f2d2a"}).json()[0]["url"]
        await self.send(image_url)

    @command
    async def shibe(self, ctx: Message):
        """Returns a random image of a Shibe"""
        image_url = requests.get("https://shibe.online/api/shibes?count=1").json()[0]
        await self.send(image_url)

    @command
    async def fortune(self, ctx: Message):
        """Returns a random fortune"""
        req = requests.get("http://yerkee.com/api/fortune").json()["fortune"]
        line = req.replace('\n','').replace('\t','')
        await self.send(line)

    @command
    async def joke(self, ctx: Message):
        """Tells a joke"""
        req = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()["joke"]
        line = " ".join(req.splitlines())
        await self.send(line)

    @command
    async def insult(self, ctx: Message, *, other_user: User = ctx.author):
        """Insults the user you mentioned"""
        req = requests.get("https://insult.mattbas.org/api/insult")
        html = req.content.decode("utf-8")
        await self.send(f"{other_user}, {req.content}.")

    @command
    async def compliment(self, ctx: Message, *, other_user: User = ctx.author):
        """Compliments the user you mentioned"""
        req = requests.get("http://www.madsci.org/cgi-bin/lynn/jardin/SCG")
        html = req.content
        soup = BeautifulSoup(html, "html.parser")
        await self.send(f"{other_user}, {soup.h2.string.strip()}")

    @command
    async def choose(self, ctx: Message, *, message):
        """Chooses a random option (separated by comma)"""
        await self.send(random.choice(message.replace(", ", ",").split(",")))

    @command
    async def roll(self, ctx: Message, *, sides: int):
        """Rolls a dice"""
        await self.send("You rolled ... " + str(random.randint(1, sides)))

    @command
    async def gh(self, ctx: Message, *, query: str):
        """Searches for a GitHub repo"""
        repo = requests.get("https://api.github.com/search/repositories?q=" + query).json()
        await self.send("Best match: " + repo["items"][0]["html_url"])

    # End of new commands

    @command
    async def funfact(self, ctx: Message):
        """Returns a random fun fact"""
        res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        await self.send(res.json()["text"])

    @command
    async def define(self, ctx: Message, *, term: str):
        """Searches for the specified term on Urban Dictionary"""
        api = "http://api.urbandictionary.com/v0/define"
        # Send request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", term)]).json()
        # Get results
        result_list = response["list"][0]

        if result_list == []:
            await self.send(f"Couldn't find any results for {term} on Urban Dictionary")
            return

        defin = result_list["definition"]
        example = result_list["example"]

        if "2." in defin:  # If there is a second definition splits data
            defin = result_list["definition"].split("2.")  # Splits data
            defin = defin[0]  # Sets defin as first definition

        if "2." in example:  # If there is a second example splits data
            example = result_list["example"].split("2.")  # Splits data
            example = example[0]  # Sets defin as first example

        if len(example) > 250 or len(defin) > 250:   # Sets a 250 character limit
            example = example[:250]
            defin = defin[:250]

        await self.send((f"Results for '{term}' on Urban Dictionary: • Definition: {defin} • Example: {example}"))

    @command
    async def covid(self, ctx: Message, *, country=None):
        """Sends COVID stats for the specified country :coronaS:"""
        # TODO: if country == None then get global stats, need to wait for dogehouse.py to get that
        country = string.capwords(country)
        if "Of" in country:
            country = country.replace("Of", "of")
            print(country)

        cases = Covid().get_status_by_country_name(country.lower())

        region = cases["country"]
        confirmed = cases["confirmed"]
        active = cases["active"]
        deaths = cases["deaths"]
        recovered = cases["recovered"]

        await self.send(f"COVID stats for {region} • Confirmed Cases: {confirmed} • Active Cases: {active} • Deaths: {deaths} • Recovered: {recovered}")

    @event
    async def on_user_join(self, user: User):
        joined = [user.id]
        await self.send(message=f"Welcome {user.mention}\u200B! I am DogeBoss, a chatbot for DogeHouse, to see my commands type: {self.prefix}help", whisper=joined)

    @command
    async def uptime(self, ctx: Message):
        """Shows for how long the bot has been online"""
        delta_uptime = datetime.utcnow() - launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        await self.send(f"I've been online for {days} day(s), {hours} hour(s), {minutes} minute(s), and {seconds} second(s)")

    @command
    async def math(self, ctx: Message, *, expression: str):
        """Returns the results for a mathematical example :5Head:"""
        # regex filter so we make sure that no character from the alphabet gets eval'd (thanks Erlend)
        filtering = re.search("[a-zA-Z]", expression)
        if filtering == None:  # filtering is None when the user passes the regex check
            calculation = eval(expression)  # evaluates the math example
            await self.send('Math: {}ㅤㅤ•ㅤㅤAnswer: {}'.format(expression, calculation))
        else:
            await self.send('You can type only numbers and operators (0-9, *, -, +, /, .)')

    @command
    async def echo(self, ctx: Message, *, message):
        """Repeats what you said"""
        await self.send(message)

    @command
    async def pp(self, ctx: Message, *, user: User):
        """Shows the tagged user's PP :gachiHYPER:"""

        pp_length = random.randrange(-1, 16)

        if pp_length == -1:
            pprnd = "girl moment :SillyChamp:"
        else:
            pprnd = "8" + "=" * pp_length + "D"

        await self.send(f"{user}'s PP: ㅤㅤㅤ{pprnd}")

    @command
    async def userinfo(self, ctx: Message, user: User = ctx.author):
        """Gets info about the user you mentioned, or you if no user is specified"""
        await self.send(f"Username: {user.mention}  •  Display Name: {user.displayname}  •  ID: {user.id}")

    @command
    async def fight(self, ctx: Message, *, other_user: User):
        """Starts a fight the user you mentioned :hyperHammer:"""

        user1 = ctx.author.mention

        if user1 == other_user:
            await self.send("Damn, you wanna kill yourself? :Sadge: I won't stop you I guess...")
            await asyncio.sleep(2.5)
            suicresp = [f'{user1} has put a gun to his head and pulled the trigger :Sadge:',
                        f'{user1} has drowned in the river next to his house.',
                        f'{user1} tried to swim in lava, S :OMEGALUL: BAD',
                        f'The shells from a shotgun pierced {user1}\'s head.']
            suicresptext = random.choice(suicresp)
            await self.send(f'{suicresptext}')
            return

        win = random.choice([user1, other_user])
        if win == user1:
            lose = other_user

        else:
            lose = user1

        responses = [f'That was an intense battle, {win} has beaten {lose} to death!', f'That was a shitty battle, they both fought themselves to death',
                     f'You call that a battle? You both suck!', f'Yo, {lose} you lose! Ha.', f'I\'m not sure how, but {win} has won the battle!', f'{lose} died whilst fighting {win}.']
        response = random.choice(responses)

        await self.send(response)

    def split_list(self, a_list):
        half = len(a_list)//2
        return a_list[:half], a_list[half:]

    @command
    async def help(self, ctx: Message):
        """Teaches you what different commands do"""
        user = [ctx.author.id]
        
        helparray = []
        this = self.__class__
        for key in this.__dict__:
            if hasattr(this.__dict__[key], '__call__'):
                function = this.__dict__[key]

                # Functions that are not commands should be excluded
                if function.command == None:
                    return

                # Get argument names and surround them with <>
                varnames = inspect.getfullargspec(function).args
                varnames.remove("self")
                varnames_formatted = ' '.join('<' + item + '>' for item in varnames)

                helpstring = f"{self.prefix}{function.__name__} {varnames_formatted}  -  {function.__doc__}"
                helparray.append(helpstring)

        # Split the help page into 2 messages
        help1, help2 = self.split_list(helparray)
        await self.send("Hey, these are my commands right now! • " + ' • '.join(help1), whisper=user)
        await asyncio.sleep(1.5)
        await self.send(' • '.join(help2), whisper=user)


if __name__ == "__main__":
    Client(DOGETOKEN, DOGEREFRESHTOKEN, prefix="d!").run()
    if run_on_repl == True:
        keep_alive()
