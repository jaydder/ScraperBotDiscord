async def setup(bot, help_service):
    from bot.cogs.help_cog import HelpCog

    await bot.add_cog(HelpCog(bot, help_service))
