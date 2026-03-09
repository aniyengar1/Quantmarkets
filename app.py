#!/bin/bash
# QuantMarkets — cron health check & setup
# Run this once to verify everything is working:
#   bash ~/Documents/quantmarkets/check_cron.sh

echo "=== QuantMarkets Cron Health Check ==="
echo ""

# 1. Check if cron job exists
echo "--- Current crontab ---"
crontab -l 2>/dev/null || echo "(no crontab set)"
echo ""

# 2. If not set, install it
CRON_LINE="0 * * * * /opt/anaconda3/bin/python3 ~/Documents/quantmarkets/collector.py >> ~/Documents/quantmarkets/collector.log 2>&1"
EXISTING=$(crontab -l 2>/dev/null | grep "collector.py")

if [ -z "$EXISTING" ]; then
    echo "⚠️  Cron job not found. Installing..."
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "✅ Cron job installed."
else
    echo "✅ Cron job already exists."
fi

echo ""

# 3. Check last 10 log lines
echo "--- Last 10 collector log lines ---"
if [ -f ~/Documents/quantmarkets/collector.log ]; then
    tail -10 ~/Documents/quantmarkets/collector.log
else
    echo "(no log file yet — run collector manually first)"
fi

echo ""

# 4. Run collector now and show output
echo "--- Running collector now ---"
/opt/anaconda3/bin/python3 ~/Documents/quantmarkets/collector.py

echo ""
echo "=== Done ==="