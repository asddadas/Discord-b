"""
Configuration file for the Discord bot
"""

# Mention tracking configuration
TARGET_CHANNEL_ID = 1388050230842232832  # Channel ID for mention tracking
TARGET_ROLE_ID = 1394407546600689754     # Role ID to assign after threshold
TAG_THRESHOLD = 5                        # Number of mentions required

# Giveaway configuration
GIVEAWAY_EMOJI = "🎉"                   # Emoji for giveaway reactions
MAX_GIVEAWAY_DURATION = 7 * 24 * 60 * 60  # 7 days in seconds
MIN_GIVEAWAY_DURATION = 60              # 1 minute in seconds

# Server management permissions
ADMIN_PERMISSIONS = ["administrator", "manage_guild", "manage_roles"]
MODERATOR_PERMISSIONS = ["kick_members", "ban_members", "manage_messages"]

# Embed colors (in hex)
COLORS = {
    "success": 0x00ff00,
    "error": 0xff0000,
    "info": 0x0099ff,
    "warning": 0xffaa00,
    "giveaway": 0xff6b6b
}

# Time format for displays
TIME_FORMAT = "%Y-%m-%d %H:%M:%S UTC"

# Database configuration
DATABASE_PATH = "bot_data.db"

# Media moderation configuration
MEDIA_ONLY_CHANNELS = []  # List of channel IDs that only allow media
ALLOWED_MEDIA_TYPES = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff',  # Images
    '.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm', '.mkv',    # Videos
    '.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'            # Audio (optional)
]
