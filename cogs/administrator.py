import discord
from discord.ext import commands
from ui.admin_panel_view import AdminPanelView, get_embed


class Administrator(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Вызывает админ панель")
    @commands.has_permissions(administrator=True)
    async def sudo(self, ctx: discord.ApplicationContext):
        view = AdminPanelView()
        embed = await get_embed()

        await ctx.respond(view=view, embed=embed, ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Administrator(bot))
