import discord
from discord.ext import commands
from config import TOKEN, PREFIX, BOT_NAME, EMBED_COLOR
from logic import (
    setup_database,
    get_recommendation,
    add_rating,
    get_average_rating,
    get_genres
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ================== EVENT ==================
@bot.event
async def on_ready():
    setup_database()
    print(f"{BOT_NAME} aktif sebagai {bot.user}")

# ================== VIEW PILIH TIPE ==================
class TipeView(discord.ui.View):
    @discord.ui.button(label="🎬 Film", style=discord.ButtonStyle.primary)
    async def film(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Pilih genre:",
            view=GenreView("film"),
            ephemeral=True
        )

    @discord.ui.button(label="📺 Serial", style=discord.ButtonStyle.success)
    async def serial(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Pilih genre:",
            view=GenreView("serial"),
            ephemeral=True
        )

# ================== VIEW GENRE ==================
class GenreView(discord.ui.View):
    def __init__(self, tipe):
        super().__init__(timeout=60)
        self.tipe = tipe

        for genre in get_genres():
            self.add_item(GenreButton(genre, tipe))

class GenreButton(discord.ui.Button):
    def __init__(self, genre, tipe):
        super().__init__(
            label=genre.capitalize(),
            style=discord.ButtonStyle.secondary
        )
        self.genre = genre
        self.tipe = tipe

    async def callback(self, interaction: discord.Interaction):
        data = get_recommendation(self.tipe, self.genre)
        if not data:
            await interaction.response.send_message("❌ Data tidak ada", ephemeral=True)
            return

        movie_id, title = data
        avg = get_average_rating(movie_id)
        rating_text = f"⭐ {avg}/5" if avg else "Belum ada rating"

        embed = discord.Embed(
            title="🎬 Rekomendasi",
            description=f"**{title}**",
            color=EMBED_COLOR
        )
        embed.add_field(name="Tipe", value=self.tipe.capitalize())
        embed.add_field(name="Genre", value=self.genre.capitalize())
        embed.add_field(name="Rating", value=rating_text, inline=False)

        await interaction.response.send_message(
            embed=embed,
            view=RatingView(movie_id),
            ephemeral=True
        )

# ================== VIEW RATING ==================
class RatingView(discord.ui.View):
    def __init__(self, movie_id):
        super().__init__(timeout=60)
        self.movie_id = movie_id

        for i in range(1, 6):
            self.add_item(RatingButton(i, movie_id))

class RatingButton(discord.ui.Button):
    def __init__(self, rating, movie_id):
        super().__init__(label=f"⭐ {rating}", style=discord.ButtonStyle.success)
        self.rating = rating
        self.movie_id = movie_id

    async def callback(self, interaction: discord.Interaction):
        add_rating(self.movie_id, interaction.user.id, self.rating)
        avg = get_average_rating(self.movie_id)

        await interaction.response.send_message(
            f"✅ Rating **{self.rating}⭐** disimpan!\n"
            f"⭐ Rata-rata sekarang: **{avg}/5**",
            ephemeral=True
        )

# ================== COMMAND ==================
@bot.command(name="movie")
async def movie(ctx):
    embed = discord.Embed(
        title=BOT_NAME,
        description="Pilih tipe tontonan:",
        color=EMBED_COLOR
    )
    await ctx.send(embed=embed, view=TipeView())

# ================== RUN ==================
bot.run(TOKEN)