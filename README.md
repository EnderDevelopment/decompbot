# DecompBot Discord Bot

DecompBot is a Discord bot for Roblox development workflows that provides slash commands for bot availability control, configured Roblox game ID listing, status checks, and best-effort Luau script template generation. It does not perform actual Roblox game decompilation and cannot guarantee that generated scripts will function as decompiled source.

## Install

1. Install Python 3.10 or newer.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.
4. Set `DISCORD_TOKEN` to the token for your Discord bot.
5. Optionally configure bot owners with comma-separated Discord user IDs:

```env
BOT_OWNER_IDS=123456789012345678,987654321098765432
```

6. Optionally configure Roblox place IDs and labels using comma-separated `place_id:label` entries:

```env
DECOMPILED_GAMES=123456:Example Game,789012:Another Game
```

7. Invite the bot to a Discord server with permission to use applications and send messages.
8. Start the bot:

```bash
python main.py
```

## Use

Use these Discord slash commands:

- `/generate_script game_id:<Roblox place ID> feature:<behavior to recreate>` generates an ephemeral `.lua` file containing a best-effort Luau script template.
- `/game_ids` displays the configured Roblox place IDs and labels.
- `/status` displays whether DecompBot functionality is enabled.
- `/disable` disables bot functionality until it is enabled again. Only configured bot owners or the Discord server owner can use it.
- `/enable` enables bot functionality. Only configured bot owners or the Discord server owner can use it.

The generated script includes comments identifying the requested place and behavior. It is a template for manual recreation, not a recovered or working copy of Roblox scripts. The bot does not retrieve, extract, or decompile protected game source code.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/a268f031-79ef-431f-87f1-b3e5776f290c?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=a268f031-79ef-431f-87f1-b3e5776f290c
