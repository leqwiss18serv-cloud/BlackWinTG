# Troubleshooting Guide - Black Win Bot

## Common Issues and Solutions

### Bot Issues

#### Bot doesn't start / No response
**Symptoms**: Bot doesn't respond to /start, no messages received

**Solutions**:
1. Check if bot is running:
   - In Replit: Look for "Bot started successfully!" in console
   - Locally: Check terminal for errors

2. Verify bot token:
   ```bash
   # Check .env file
   cat .env | grep BOT_TOKEN
   ```
   - Should start with a long number followed by colon
   - Get new token from @BotFather if needed

3. Check network connection:
   - Telegram API must be accessible
   - Replit might be down (check status.replit.com)

4. Restart the bot:
   - In Replit: Click "Stop" then "Run"
   - Locally: Ctrl+C then `python main.py`

#### Bot responds but commands don't work
**Symptoms**: Bot receives messages but doesn't execute commands

**Solutions**:
1. Check user registration:
   - Send `/start` first
   - Check database for user entry

2. Verify database connection:
   - Check SUPABASE_URL and SUPABASE_KEY
   - Test Supabase dashboard accessibility

3. Check logs for errors:
   - Look for Python tracebacks
   - Database connection errors

### Database Issues

#### "Database error" messages
**Symptoms**: Bot responds with database-related errors

**Solutions**:
1. Verify Supabase credentials:
   ```bash
   # Should be set in .env
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_KEY=eyJ...
   ```

2. Check if tables exist:
   - Go to Supabase dashboard
   - Click "Table Editor"
   - Verify all tables from DATABASE.md exist

3. Check table permissions:
   - In Supabase, go to "Authentication" → "Policies"
   - Ensure service role can access tables

4. Test database connection:
   ```python
   # Test script
   from supabase import create_client
   client = create_client("YOUR_URL", "YOUR_KEY")
   result = client.table('users').select('*').limit(1).execute()
   print(result)
   ```

#### User not found after /start
**Symptoms**: Used /start but profile shows as not registered

**Solutions**:
1. Check for SQL errors in logs
2. Verify user table has no constraints blocking insertion
3. Try manual user creation in Supabase dashboard
4. Check if user ID is being passed correctly

### Game Issues

#### Bets not working
**Symptoms**: Can't place bets, balance doesn't update

**Solutions**:
1. Check minimum bet amount (100 BC default)
2. Verify user has sufficient balance
3. Check if user is banned: `/profile` → look for ban status
4. Review logs for transaction errors

#### Balance stuck / not updating
**Symptoms**: Win a game but balance doesn't change

**Solutions**:
1. Check database.py update_balance function
2. Verify no database errors in logs
3. Refresh by running another command
4. Check database directly in Supabase

#### Games give wrong results
**Symptoms**: Wrong multipliers, incorrect outcomes

**Solutions**:
1. Check utils/helpers.py game logic
2. Verify event multipliers (x2 WIN affects results)
3. Check if bet amount matches displayed amount
4. Review game-specific code in handlers/games.py

### Economy Issues

#### Daily bonus not working
**Symptoms**: Can't claim daily bonus or timer wrong

**Solutions**:
1. Check last_daily timestamp in database
2. Verify 24-hour cooldown logic
3. Check timezone issues (UTC vs local)
4. Test with manual timestamp update:
   ```sql
   UPDATE users SET last_daily = NOW() - INTERVAL '25 hours' WHERE id = YOUR_ID;
   ```

#### Promo codes not activating
**Symptoms**: Valid promo shows as invalid

**Solutions**:
1. Check promo exists in database:
   ```sql
   SELECT * FROM promocodes WHERE code = 'YOUR_CODE';
   ```

2. Verify not expired:
   - Check expires_at timestamp
   - Compare with current time

3. Check usage limit:
   - uses < max_uses?
   - User hasn't used it already?

4. Create new promo to test:
   ```
   /createpromo TEST 1000 10
   ```

#### Bank interest not calculating
**Symptoms**: Money in bank but no interest

**Solutions**:
1. Bank interest is manual (not automated yet)
2. Can be run as scheduled job
3. SQL to apply interest:
   ```sql
   UPDATE users 
   SET bank_balance = bank_balance * 1.05,
       last_bank_interest = NOW()
   WHERE last_bank_interest < NOW() - INTERVAL '24 hours';
   ```

### Permission Issues

#### "Permission denied" / "Access forbidden"
**Symptoms**: Can't access admin commands

**Solutions**:
1. Verify OWNER_ID matches your Telegram ID:
   - Get ID from @userinfobot
   - Check .env file

2. Check database role:
   ```sql
   SELECT id, username, role FROM users WHERE id = YOUR_ID;
   ```

3. Manually set role if needed:
   ```sql
   UPDATE users SET role = 'owner' WHERE id = YOUR_ID;
   ```

4. Restart bot after role change

#### Can't ban users
**Symptoms**: Ban command doesn't work

**Solutions**:
1. Verify you're owner (not just admin)
2. Check command syntax: `/ban USER_ID reason here`
3. Ensure user exists in database
4. Check logs for errors

### Deployment Issues (Replit)

#### Bot stops after inactivity
**Symptoms**: Bot works then stops after 1 hour

**Solutions**:
1. Set up UptimeRobot:
   - Create free account at uptimerobot.com
   - Add HTTP monitor for your Repl URL
   - Set interval to 5 minutes

2. Enable Always On (Paid):
   - Replit Hacker plan
   - Toggle "Always On" in Repl settings

3. Keep-alive server issues:
   - Check if Flask server running (port 8080)
   - Verify keep_alive() called in main.py
   - Check firewall isn't blocking port

#### "Secrets not found"
**Symptoms**: Environment variables not loading

**Solutions**:
1. In Replit, click "Secrets" (lock icon)
2. Add all required secrets:
   - BOT_TOKEN
   - SUPABASE_URL
   - SUPABASE_KEY
   - OWNER_ID
   - OWNER_USERNAME

3. Restart Repl after adding secrets

4. For local development, use .env file instead

### Performance Issues

#### Bot slow to respond
**Symptoms**: Delays in bot responses

**Solutions**:
1. Check database query performance
2. Add indexes if missing (see DATABASE.md)
3. Reduce concurrent users (if using free tier)
4. Optimize game logic
5. Check Replit/Supabase status pages

#### Memory errors
**Symptoms**: Bot crashes with memory errors

**Solutions**:
1. Restart bot/Repl
2. Check for memory leaks
3. Upgrade Replit plan if needed
4. Optimize code (reduce data stored in memory)

## Debug Mode

Enable detailed logging:

```python
# In main.py, change logging level
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Getting Help

### Before Asking for Help

1. Check this guide
2. Review SETUP.md
3. Check logs for errors
4. Try restarting bot
5. Verify all credentials

### Where to Get Help

1. **GitHub Issues**: Report bugs at https://github.com/leqwiss18serv-cloud/BlackWinTG/issues
2. **Telegram**: Contact @kLeqwiss
3. **Documentation**: Read README.md, SETUP.md, DATABASE.md

### Information to Provide

When asking for help, include:
- Error messages (full traceback)
- Steps to reproduce
- Your environment (Replit/Local, Python version)
- What you've already tried
- Relevant configuration (don't share secrets!)

## Testing Checklist

After fixing issues, test:

- [ ] /start - Bot responds with welcome
- [ ] /profile - Shows user profile
- [ ] /games - Shows games menu
- [ ] Play a simple game (50/50)
- [ ] /balance - Shows correct balance
- [ ] /bank - Can deposit/withdraw
- [ ] /daily - Can claim once per 24h
- [ ] /top - Shows leaderboard
- [ ] /shop - Can open cases
- [ ] /admin - Access (if owner/admin)
- [ ] /stats - Shows bot stats (if owner)

## Prevention Tips

1. **Regular Backups**: Export Supabase database weekly
2. **Monitor Logs**: Check for errors daily
3. **Test Changes**: Test in private before deploying
4. **Keep Updated**: Update dependencies when needed
5. **Document Changes**: Note any customizations
6. **Version Control**: Use git for all changes

## Emergency Procedures

### Bot Completely Broken

1. Stop the bot
2. Backup database (export from Supabase)
3. Check git history for recent changes
4. Revert to last working commit
5. Restart bot
6. Test basic functionality
7. Gradually restore features

### Database Corrupted

1. Stop all bots accessing database
2. Export current data if possible
3. Restore from backup
4. Verify data integrity
5. Restart bot
6. Monitor for issues

### Lost Access

1. Verify credentials in .env / Replit Secrets
2. Check @BotFather for bot status
3. Verify Supabase project status
4. Create new bot if needed (change token)
5. Don't share credentials

---

**Still having issues?** Contact @kLeqwiss on Telegram with:
- Description of problem
- Error messages
- What you've tried
- Screenshots if relevant
