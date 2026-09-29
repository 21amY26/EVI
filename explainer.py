"""EVI Bot Explanation Module."""
def show_help():
    print("""
EVI Help:

1. Forensic Scan - Analyse the whole log file once
2. Live Monitor  - Follow the file like `tail -f` and flag gaps in new lines
3. Hybrid        - Forensic scan, then keep following the file
4. Help
0. Exit

Gaps (time with no log entries, flagged above 30s):
  LOW       30-60s   normal system delay
  MEDIUM    1-5 min  unusual, worth checking
  CRITICAL  > 5 min  likely tampering or deleted logs

Out-of-order timestamps (a line older than the one before it) are
flagged separately as a sign of edited or injected entries.

Press ENTER to return...
""")
    input()
