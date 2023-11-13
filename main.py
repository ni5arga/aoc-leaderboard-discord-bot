import os
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand
import requests

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
AOC_LEADERBOARD_ID = os.environ.get('AOC_LEADERBOARD_ID')
CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID'))

bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@slash.slash(name='leaderboard', description='Get Advent of Code leaderboard stats')
@slash.slash(name='lb', description='Get Advent of Code leaderboard stats (alias for /leaderboard)')
async def leaderboard(ctx):
    url = f'https://adventofcode.com/2023/leaderboard/private/view/{AOC_LEADERBOARD_ID}.json'
    headers = {'Cookie': f'session={os.environ.get("AOC_SESSION_COOKIE")}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        leaderboard_members = data['members']

        stats = []
        for member_id, member_data in leaderboard_members.items():
            member_name = member_data['name']
            member_star_count = member_data['stars']
            member_local_score = member_data['local_score']
            stats.append(f"{member_name}: {member_star_count} stars, {member_local_score} points")

        await ctx.send('\n'.join(stats))
    else:
        await ctx.send(f'Failed to fetch leaderboard. Status code: {response.status_code}')

@slash.slash(name='top', description='Get top 10 players from Advent of Code leaderboard')
async def top(ctx):
    url = f'https://adventofcode.com/2023/leaderboard/private/view/{AOC_LEADERBOARD_ID}.json'
    headers = {'Cookie': f'session={os.environ.get("AOC_SESSION_COOKIE")}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        leaderboard_members = data['members']

        top_players = sorted(leaderboard_members.items(), key=lambda x: x[1]['local_score'], reverse=True)[:10]
        top_stats = []
        for member_id, member_data in top_players:
            member_name = member_data['name']
            member_star_count = member_data['stars']
            member_local_score = member_data['local_score']
            top_stats.append(f"{member_name}: {member_star_count} stars, {member_local_score} points")

        await ctx.send('\n'.join(top_stats))
    else:
        await ctx.send(f'Failed to fetch leaderboard. Status code: {response.status_code}')

@slash.slash(name='global', description='Get top 10 players from global Advent of Code leaderboard')
async def global_leaderboard(ctx):
    url = f'https://adventofcode.com/2023/leaderboard/public/global.json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        leaderboard_members = data['members']

        global_top_players = sorted(leaderboard_members.items(), key=lambda x: x[1]['local_score'], reverse=True)[:10]
        global_top_stats = []
        for member_id, member_data in global_top_players:
            member_name = member_data['name']
            member_star_count = member_data['stars']
            member_local_score = member_data['local_score']
            global_top_stats.append(f"{member_name}: {member_star_count} stars, {member_local_score} points")

        await ctx.send('\n'.join(global_top_stats))
    else:
        await ctx.send(f'Failed to fetch global leaderboard. Status code: {response.status_code}')

@bot.command(name='leaderboard', aliases=['lb'])
async def cmd_leaderboard(ctx):
    await ctx.invoke(bot.get_command('leaderboard'))

@bot.command(name='top')
async def cmd_top(ctx):
    await ctx.invoke(bot.get_command('top'))

@bot.command(name='global')
async def cmd_global(ctx):
    await ctx.invoke(bot.get_command('global'))

@bot.command(name='help')
async def help_command(ctx):
    help_message = (
        'Available Commands:\n'
        '`/leaderboard` or `/lb`: Get Advent of Code leaderboard stats.\n'
        '`/top`: Get top 10 players from Advent of Code leaderboard.\n'
        '`/global`: Get top 10 players from global Advent of Code leaderboard.\n'
        '`!leaderboard` or `!lb`: Get Advent of Code leaderboard stats.\n'
        '`!top`: Get top 10 players from Advent of Code leaderboard.\n'
        '`!global`: Get top 10 players from global Advent of Code leaderboard.\n'
        '`!help`: Display this help message.'
    )
    await ctx.send(help_message)

bot.run(TOKEN)
