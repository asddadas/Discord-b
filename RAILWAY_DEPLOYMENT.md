# Discord Bot Deployment Guide - Railway

This guide will help you deploy your Discord bot on Railway for 24/7 hosting.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Discord Bot Token**: Your bot token from Discord Developer Portal
3. **Database**: Railway provides PostgreSQL automatically

## Step 1: Prepare Your Project

Your bot is already configured for Railway deployment with:
- `main.py` with web server for health checks
- PostgreSQL database support
- Environment variable configuration
- Proper async handling

## Step 2: Create Railway Project

1. **Connect Repository**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Choose "Deploy from GitHub repo"
   - Connect your GitHub account and select your repository

2. **Alternative - Deploy from Template**:
   - Upload your project files to GitHub first
   - Use Railway's GitHub integration

## Step 3: Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```
DISCORD_BOT_TOKEN=your_bot_token_here
```

**Important**: Never commit your bot token to GitHub!

## Step 4: Database Setup

Railway automatically provides PostgreSQL:
- Database URL is automatically set as `DATABASE_URL`
- No additional configuration needed
- Your bot will auto-create tables on startup

## Step 5: Configure Deployment

Railway automatically detects Python projects. If needed, create these files:

### `railway.toml` (optional)
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python main.py"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### `Procfile` (optional)
```
web: python main.py
```

## Step 6: Deploy

1. **Automatic Deployment**:
   - Railway will automatically build and deploy
   - Watch the build logs in the Railway dashboard
   - Deployment typically takes 2-3 minutes

2. **Manual Deployment**:
   - Push changes to your GitHub repository
   - Railway will automatically redeploy

## Step 7: Verify Deployment

1. **Check Health Endpoint**:
   - Your bot runs a web server on port 5000
   - Railway will provide a URL like `https://your-app.railway.app`
   - Visit the URL to see "Discord Bot is running"

2. **Check Discord**:
   - Your bot should appear online in Discord
   - Test with `!ping` command

## Configuration Details

### Port Configuration
```python
# Your bot already handles this correctly
PORT = int(os.getenv('PORT', 5000))
```

### Database Connection
```python
# Already configured - uses DATABASE_URL automatically
DATABASE_URL = os.getenv('DATABASE_URL')
```

## Troubleshooting

### Common Issues

1. **Bot Token Missing**:
   - Check Environment Variables in Railway dashboard
   - Ensure `DISCORD_BOT_TOKEN` is set correctly

2. **Database Connection Issues**:
   - Railway provides PostgreSQL automatically
   - Check if `DATABASE_URL` is available in variables

3. **Build Failures**:
   - Check build logs in Railway dashboard
   - Ensure `pyproject.toml` has all dependencies

4. **Bot Offline**:
   - Check application logs in Railway
   - Verify bot token is valid
   - Check Discord bot permissions

### Useful Commands

```bash
# Check logs
railway logs

# Run locally (if Railway CLI installed)
railway run python main.py

# Deploy specific service
railway up
```

## Cost Information

Railway Pricing:
- **Hobby Plan**: $5/month - Good for personal bots
- **Pro Plan**: $20/month - For production use
- **Free Tier**: Limited hours (good for testing)

## Monitoring

Railway provides:
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Application and build logs
- **Health Checks**: Automatic health monitoring
- **Alerts**: Email notifications for issues

## Benefits of Railway

✅ **Easy Setup**: One-click PostgreSQL database
✅ **Auto Scaling**: Handles traffic spikes
✅ **Git Integration**: Auto-deploy on push
✅ **Zero Downtime**: Rolling deployments
✅ **SSL/HTTPS**: Automatic certificates
✅ **Monitoring**: Built-in metrics and logs

## Next Steps

After deployment:
1. Monitor your bot's performance in Railway dashboard
2. Set up alerts for downtime
3. Configure custom domain (optional)
4. Set up automated backups for important data

Your Discord bot is now ready for 24/7 hosting on Railway!