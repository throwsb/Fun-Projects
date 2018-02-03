#!/usr/bin/env python3

LOGFILE="./TMLog"
LOGFILE="./TMLog"
TMINCLUDE="./TMInclude"
TMEXCLUDE="./TMExclude"
BKUPDIR="/BACKUP/"
RSYNC="/usr/bin/rsync"
RSYNC_OPTS="-azPHx --exclude-from=TMEXCLUDE --log-files=LOGFILE --delete --delete-exclude BKUPDIR"

