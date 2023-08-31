#!/usr/bin/env bash

set -e
set -o pipefail

if [ ! -f /data/etc/icinga2/conf.d/icingaweb-api-user.conf ]; then
  sed "s/\$ICINGAWEB_ICINGA2_API_USER_PASSWORD/${ICINGAWEB_ICINGA2_API_USER_PASSWORD:-icingaweb}/" /config/icingaweb-api-user.conf >/data/etc/icinga2/conf.d/icingaweb-api-user.conf
fi

if [ ! -f /data/etc/icinga2/features-enabled/icingadb.conf ]; then
  mkdir -p /data/etc/icinga2/features-enabled
  cat /config/icingadb.conf >/data/etc/icinga2/features-enabled/icingadb.conf
fi

if [ ! -f /data/etc/icinga2/custom_config_included.flag ]; then
  cat >>/data/etc/icinga2/icinga2.conf <<EOF

/** 
 * custom configuration files
 */
include_recursive "/custom_data/custom.conf.d"
EOF
  touch /data/etc/icinga2/custom_config_included.flag
fi

if [ ! -f /tmp/id_rsa ]; then
  /usr/bin/ssh-keygen -f /data/etc/icinga2/id_rsa -N ''
fi

cat /data/etc/icinga2/id_rsa.pub

if [ -f /data/etc/icinga2/conf.d/hosts.conf ] ; then
  rm -f /data/etc/icinga2/conf.d/hosts.conf
fi
