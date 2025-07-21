import discord
from discord.ext import commands
import asyncio
import logging
import os
from aiohttp import web
from config import *
from bot.mention_tracker import MentionTracker
# from bot.giveaway_system import GiveawaySystem
from bot.server_management import ServerManagement
from bot.utilities import Utilities
from bot.activity_logger import ActivityLogger
from database.database import Database

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True
intents.voice_states = True  # Required for voice channel logging

bot = commands.Bot(
    command_prefix="!", 
    intents=intents,
    help_command=None,  # Disable default help for faster responses
    case_insensitive=True,  # Allow case-insensitive commands
    strip_after_prefix=True  # Strip whitespace after prefix
)

@bot.event
async def on_ready():
    logger.info(f"Bot is ready. Logged in as {bot.user}.")
    print(f"Bot is ready. Logged in as {bot.user}.")
    
    # Initialize database
    db = Database()
    await db.initialize()
    
    # Set bot status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Revisando que no la caguen"))

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument provided: {str(error)}")
    else:
        logger.error(f"Unexpected error: {error}")
        await ctx.send("❌ An unexpected error occurred. Please try again later.")

async def health_check(request):
    """Health check endpoint for deployment"""
    return web.Response(text="Discord Bot is running", status=200)

async def start_web_server():
    """Start web server for deployment health checks"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    port = int(os.getenv('PORT', 5000))
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Try different ports if the default is in use
    for attempt_port in [port, port + 1, port + 2, 8000, 8080, 3000]:
        try:
            site = web.TCPSite(runner, '0.0.0.0', attempt_port)
            await site.start()
            logger.info(f"Web server started on port {attempt_port}")
            return runner
        except OSError as e:
            if e.errno == 98:  # Address already in use
                logger.warning(f"Port {attempt_port} is already in use, trying next port")
                continue
            else:
                raise e
    
    # If we can't find any available port, log error but continue
    logger.error("Could not find an available port for web server")
    return runner

async def main():
    """Main function to start the bot and load extensions"""
    logger.info("Starting Discord bot application...")
    
    # Start web server for deployment
    try:
        web_runner = await start_web_server()
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        web_runner = None
    
    try:
        # Get bot token from environment variable
        token = os.getenv("DISCORD_BOT_TOKEN")
        
        if not token:
            logger.error("Please set the DISCORD_BOT_TOKEN environment variable")
            return
        
        logger.info("Bot token found, starting bot...")
        
        async with bot:
            try:
                # Add cogs
                logger.info("Loading cogs...")
                await bot.add_cog(MentionTracker(bot))
                logger.info("✅ MentionTracker loaded")
                
                # await bot.add_cog(GiveawaySystem(bot))
                await bot.add_cog(ServerManagement(bot))
                logger.info("✅ ServerManagement loaded")
                
                await bot.add_cog(Utilities(bot))
                logger.info("✅ Utilities loaded")
                
                await bot.add_cog(ActivityLogger(bot))
                logger.info("✅ ActivityLogger loaded")
                
                logger.info("All cogs loaded successfully, connecting to Discord...")
                await bot.start(token)
                
            except Exception as e:
                logger.error(f"Error during bot startup: {e}")
                raise
                
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        raise
    finally:
        # Cleanup web server
        if web_runner:
            try:
                await web_runner.cleanup()
                logger.info("Web server cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up web server: {e}")
        
        logger.info("Discord bot application stopped")

if __name__ == "__main__":
    asyncio.run(main())
