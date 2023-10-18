FROM icinga/icinga2:latest

USER root

ADD check_diameter/check_diameter.py /usr/lib/nagios/plugins/check_diameter.py
ADD check_influxdb2_query/check_influxdb_query.py /usr/lib/nagios/plugins/check_influxdb_query.py

RUN apt update && \
    apt upgrade -y && \
    apt install -y make snmp less python3-pip && \
    pip3 install pyDiameter influxdb_client nagiosplugin && \
    cpan String::Random && \
    apt clean -y && \
    curl https://raw.githubusercontent.com/nguttman/Nagios-Checks/master/SIP/check_sip2 \
      -o /usr/lib/nagios/plugins/check_sip2 && \
    chmod +x /usr/lib/nagios/plugins/check_sip2 /usr/lib/nagios/plugins/check_diameter.py \
      /usr/lib/nagios/plugins/check_influxdb_query.py

VOLUME /usr/share/snmp/mibs/

USER icinga