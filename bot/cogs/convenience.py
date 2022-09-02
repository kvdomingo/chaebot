from discord import Interaction
from discord.app_commands import command, describe


@command(description="Get client latency")
async def ping(itx: Interaction):
    await itx.response.send_message(f"Pong ({round(itx.client.latency * 1000)}ms)")


@command(description="Delete the specified number of messages from the channel")
@describe(amount="Number of messages to purge")
async def purge(itx: Interaction, amount: int = 0):
    if amount < 1:
        await itx.response.send_message("Please specify a positive number.")
    else:
        await itx.channel.purge(limit=amount + 1)
