#!/usr/bin/env bash

CONTAINER=$1
STATISTIC=$2
WARN_LEVEL=$3
CRIT_LEVEL=$4

VALUE=`/usr/bin/docker exec $CONTAINER /usr/sbin/kamcmd stats.get_statistics $STATISTIC | /bin/sed 's:.*=\s*\([0123456789]\+\):\1:g'`

if [ -z "$VALUE" ]; then
  echo "UNKNOWN: no output statistic $STATISTIC"
  exit 3
fi

if [ $VALUE -lt $CRIT_LEVEL ]; then
  echo "CRITICAL: statistic $STATISTIC below critical level: $VALUE"
  exit 2
fi

if [ $VALUE -lt $WARN_LEVEL ]; then
  echo "WARNING: statistic $STATISTIC below warning level: $VALUE"
  exit 1
fi

if [ $VALUE -ge $WARN_LEVEL ]; then
  echo "OK: statistic $STATISTIC above warning level: $VALUE"
  exit 0
fi

echo "UNKNOWN: can't parse get_statistic output: $VALUE"
exit 3