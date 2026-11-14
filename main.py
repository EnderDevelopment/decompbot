"""DecompBot: Discord commands for best-effort Roblox script generation."""

from __future__ import annotations

import io
import os
from dataclasses import dataclass

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def parse_ids(value: str) -> set[int]:
    """Parse a comma-separated list of Discord user IDs."""
    result: set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if item.isdigit():
            result.add(int(item))
    return result


@dataclass(frozen=True)
class GameEntry:
    place_id: int
    label: str


def parse_games(value: str) -> list[GameEntry]:
    """Parse configured Roblox place IDs in place_id:label format."""
    games: list[GameEntry] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        place_id_text, _, label = item.partition(":")
        if place_id_text.strip().isdigit():
            games.append(GameEntry(int(place_id_text.strip()), label.strip() or "Unnamed game"))
    return games


TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
OWNER_IDS = parse_ids(os.getenv("BOT_OWNER_IDS", ""))
GAME_ENTRIES = parse_games(os.getenv("DECOMPILED_GAMES", ""))


class DecompBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.enabled = True

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        if self.user is not None:
            print(f"Logged in as {self.user} ({self.user.id})")


bot = DecompBot()


def owner_only(interaction: discord.Interaction) -> bool:
    if interaction.user.id in OWNER_IDS:
        return True
    return interaction.guild is not None and interaction.user.id == interaction.guild.owner_id


def unavailable_message() -> str:
    return "DecompBot functionality is currently disabled by an owner."


@bot.tree.command(name="disable", description="Disable DecompBot commands until enabled again.")
async def disable(interaction: discord.Interaction) -> None:
    if not owner_only(interaction):
        await interaction.response.send_message("Only configured bot owners or the server owner can do that.", ephemeral=True)
        return
    bot.enabled = False
    await interaction.response.send_message("DecompBot functionality is now disabled.")


@bot.tree.command(name="enable", description="Enable DecompBot commands.")
async def enable(interaction: discord.Interaction) -> None:
    if not owner_only(interaction):
        await interaction.response.send_message("Only configured bot owners or the server owner can do that.", ephemeral=True)
        return
    bot.enabled = True
    await interaction.response.send_message("DecompBot functionality is now enabled.")


@bot.tree.command(name="generate_script", description="Generate a best-effort Roblox Luau script template.")
@app_commands.describe(game_id="Roblox place ID", feature="Feature or behavior to recreate")
async def generate_script(interaction: discord.Interaction, game_id: str, feature: str) -> None:
    if not bot.enabled:
        await interaction.response.send_message(unavailable_message(), ephemeral=True)
        return
    if not game_id.isdigit():
        await interaction.response.send_message("game_id must contain only digits.", ephemeral=True)
        return
    feature = feature.strip()
    if not feature or len(feature) > 120:
        await interaction.response.send_message("feature must be between 1 and 120 characters.", ephemeral=True)
        return

    script = f'''-- DecompBot best-effort script for Roblox place {game_id}
-- Requested behavior: {feature}
-- Decompiled output may be incomplete and may require manual fixes.

local Players = game:GetService("Players")

local function initialize()
    -- Recreate the requested behavior here: {feature}
    -- Validate remotes, services, and object paths against the target place.
    print("Generated script initialized for place {game_id}")
end

initialize()
'''
    file = discord.File(io.BytesIO(script.encode("utf-8")), filename=f"decomp_{game_id}.lua")
    await interaction.response.send_message(
        "Generated a best-effort Luau script. Decompiled scripts may not fully function as intended.",
        file=file,
        ephemeral=True,
    )


@bot.tree.command(name="game_ids", description="Send configured decompiled Roblox game IDs.")
async def game_ids(interaction: discord.Interaction) -> None:
    if not bot.enabled:
        await interaction.response.send_message(unavailable_message(), ephemeral=True)
        return
    if not GAME_ENTRIES:
        await interaction.response.send_message("No game IDs are configured yet.", ephemeral=True)
        return
    lines = [f"{entry.label}: `{entry.place_id}`" for entry in GAME_ENTRIES]
    await interaction.response.send_message("Configured decompiled game IDs:\n" + "\n".join(lines))


@bot.tree.command(name="status", description="Show whether DecompBot functionality is enabled.")
async def status(interaction: discord.Interaction) -> None:
    state = "enabled" if bot.enabled else "disabled"
    await interaction.response.send_message(f"DecompBot functionality is {state}.", ephemeral=True)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN is required. Copy .env.example to .env and set it.")
    bot.run(TOKEN)
