import discord, dotenv, os
from web_scraper import *

def __find_role(name: str, role_list: list[discord.Role]) -> discord.Role:
    for r in role_list:
        if r.name == name.lower():
            return r

def __test_name(name: str) -> bool:
    return (len(name) == 8 or len(name) == 9) and name[:4].isalpha() and name[4:8].isnumeric()

class StudyBot:
    intents = discord.Intents.default()
    intents.message_content = True
    client: discord.Client = discord.Client(intents=intents)
    bot: discord.Bot = discord.Bot()
    token: str = None
    
    @bot.event
    async def on_ready():
        print("bot is now online")
    
    def __init__(self):
        dotenv.load_dotenv()
        self.token = str(os.getenv("TOKEN"))
        
    def run(self):
        self.bot.run(self.token)
        
    course = bot.create_group("course", "Course-related commands")
    
    @course.command(name = "join", description = "Join an existing course channel")
    async def join_course(ctx: discord.Interaction, name: str):
        await ctx.response.defer()
        try:
            if not __test_name(name):
                await ctx.respond(f"Error: name is invalid!")
                return
            formatted_name = name.upper()
            server = ctx.guild
            role_list = server.roles
            role = __find_role(name.lower(), role_list)
            await ctx.user.add_roles(role)
            await ctx.followup.send(f"Joined {formatted_name}'s channel.")
        except Exception as e:
            await ctx.followup.send("An error has occurred. Please try again!")
            print(e)
    
    @course.command(name = "leave", description = "Leave an existing course channel")
    async def join_course(ctx: discord.Interaction, name: str):
        await ctx.response.defer()
        try:
            if not __test_name(name):
                await ctx.respond(f"Error: name is invalid!")
                return
            formatted_name = name.upper()
            server = ctx.guild
            role_list = server.roles
            role = __find_role(name.lower(), role_list)
            await ctx.user.remove_roles(role)
            await ctx.followup.send(f"Left {formatted_name}'s channel.")
        except Exception as e:
            await ctx.followup.send("An error has occurred. Please try again!")
            print(e)
    
    @course.command(name = "create", description = "Create a new course channel")
    async def create_course(ctx: discord.Interaction, name: str):
        await ctx.response.defer()
        try:
            if not __test_name(name):
                await ctx.respond(f"Error: name is invalid!")
                return
            if name.lower() in [i.name[:4] + i.name[5:] for i in ctx.guild.text_channels]:
                await ctx.respond(f"Error: channel already exists!")
                return
            channel_name = name[:4].lower() + "-" + name[4:].lower()
            formatted_name = name.upper()
            server = ctx.guild
            role_list = server.roles
            role_names = [r.name for r in role_list]
            role = None
            if name.lower() not in role_names:
                role = await server.create_role(name=name.lower(), mentionable=True)
            else:
                role = __find_role(name.lower(), role_list)
            category_list = server.categories
            category = None
            category_name = str(os.getenv("CATEGORY_NAME"))
            for c in category_list:
                if c.name == category_name:
                    category = c
                    break
            if category != None:
                channel = await server.create_text_channel(name=channel_name, category=category)
                for r in role_list:
                    await channel.set_permissions(target=r, overwrite=discord.PermissionOverwrite(read_messages=False))
                await channel.set_permissions(target=role, overwrite=discord.PermissionOverwrite(read_messages=True))
            await ctx.followup.send(f"Created channel for {formatted_name}.")
        except Exception as e:
            await ctx.followup.send("An error has occurred. Please try again!")
            print(e)
            
    @course.command(name = "list", description = "List currently existing course channels")
    async def list_course(ctx: discord.Interaction):
        await ctx.response.defer()
        channel_list = [tc.name[:4] + tc.name[5:] for tc in ctx.guild.text_channels if not ((len(tc.name) != 8 and len(tc.name) != 9) or not tc.name[:4].isalpha() or not tc.name[5:9].isnumeric())]
        msg = "List of course channels:\n```"
        for i in sorted(channel_list):
            msg += '- ' + i.upper() + '\n'
        msg.strip()
        msg += '```'
        await ctx.followup.send(msg)
        
    @course.command(name = "rev_search", description = "Reverse search whether a course is pre-requisite or co-requisite to another course")
    async def rev_search(ctx: discord.Interaction, name: str, year: str):
        await ctx.response.defer()
        if not __test_name(name):
            await ctx.respond(f"Error: name is invalid!")
            return
        msg = "Pre-requisites:"
        await ctx.followup.send(msg)

    @course.command(name = "scrape", description = "Scrapes all courses in currently viewable semesters")
    async def scrape_courses(ctx: discord.Interaction):
        await ctx.response.defer()
        scrape()
        await ctx.followup.send("Finished scraping all the courses.")