          �"Objects for Nagios(tm) events.  There are 2 primary tables
      reflecting the division in Nagios for Host events and
      Service events.

      The event tables are extended by the HostNotifyTable and the 
      ServiceNotifyTable to keep track of the notifications based on events.
      
      The tables entries themselves are not accessible but are used for OID
      entries for TRAP/INFORM notifications.

      These objects are based on the macros defined in Nagios v2.0
      " �" Subhendu Ghosh
      
      Telephone: +1 201 232 2851
      Email: sghosh@users.sourceforge.net

      Nagios Information:
        http://www.nagios.org
      " "200503090000Z" "200501200000Z" "Spell check" "Initial Version"       -- March 9, 2005
       "Table of Nagios host events"                       "Each notification event"                       �"This object uniquely identifies this host event entry.  It is generated
		by the SNMP application and is not related to any Nagios data."                       9"Hostname as specified in the Nagios configuration file."                       >"The host alias as specified in the Nagios configuration file"                       4"The host state as defined by the HOSTSTATEID macro"                       6"The host state as defined by the HOSTSTATETYPE macro"                      v"The number of the current host check retry. For instance, if this is the 
    second time that the host is being rechecked, this will be the number two. 
    Current attempt number is really only useful when writing host event 
    handlers for soft states that take a specific action based on the host retry 
    number. The host state as defined by the HOSTSTATEID macro"                       \"A number indicating the number of seconds that the host has spent in its 
   current state"                      "The short name of the hostgroup that this host belongs to. This value is 
    taken from the hostgroup_name directive in the hostgroup definition. If the 
    host belongs to more than one hostgroup this macro will contain the name of
    just one of them."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch) 
   indicating the time at which a check of the host was last performed."                       y"This is a timestamp in time_t format (seconds since the UNIX epoch)
   indicating the time the host last changed state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the host was last detected as being in an UP
    state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the host was last detected as being in an
    DOWN state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the host was last detected as being in an
    UNREACHABLE state."                       :"The text output from the last host check (i.e. Ping OK)."                       d"This object contains any performance data that may have been returned 
    by the last host check."                       $"Table of Nagios host notifications"                       n"Nagios host notifications extends the nagiosHostEventTable when a
   notification is generated for an event."                       �"This identifies the type of notification that is being sent
    (PROBLEM, RECOVERY, ACKNOWLEDGEMENT, FLAPPINGSTART or FLAPPINGSTOP)"                      �"This identifies the current notification number for the service or host.
		The notification number increases by one (1) each time a new notification
		is sent out for a host or service (except for acknowledgements). The 
		notification number is reset to 0 when the host or service recovers 
		(after the recovery notification has gone out). Acknowledgements do not
		cause the notification number to increase."           -- was NotifyType
           �"A string containing the name of the user who acknowledged the host 
    problem. This macro is only valid in notifications where the 
    $NOTIFICATIONTYPE$ macro is set to ACKNOWLEDGEMENT."                       �"A string containing the acknowledgement comment that was entered by 
    the user who acknowledged the host problem. This macro is only valid 
    in notifications where the $NOTIFICATIONTYPE$ macro is set to ACKNOWLEDGEMENT"                       '"Table of Nagios service notifications"                       !"Table of Nagios service events."                       :"This object uniquely identifies this service event entry"                       9"Hostname as specified in the Nagios configuration file."                       >"The host alias as specified in the Nagios configuration file"                       l"A number that corresponds to the current state of the service: 0=OK,
    1=WARNING, 2=CRITICAL, 3=UNKNOWN."                       ."Whether the host is in a hard or soft state."                       S"This value is taken from the description directive of the service
    definition."                       l" A number that corresponds to the current state of the service: 0=OK,
    1=WARNING, 2=CRITICAL, 3=UNKNOWN"                      K"The number of the current service check retry. For instance, if this is
    the second time that the service is being rechecked, this will be the
    number two. Current attempt number is really only useful when writing
    service event handlers for soft states that take a specific action based
    on the service retry number."                       `"A number indicating the number of seconds that the service has spent in
    its current state."                      "The short name of the servicegroup that this service belongs to. This
    value is taken from the servicegroup_name directive in the servicegroup
    definition. If the service belongs to more than one servicegroup this
    object will contain the name of just one of them."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which a check of the service was last performed."                       }"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time the service last changed state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the service was last detected as being in an
    OK state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the service was last detected as being in a
    WARNING state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the service was last detected as being in a
    CRITICAL state."                       �"This is a timestamp in time_t format (seconds since the UNIX epoch)
    indicating the time at which the service was last detected as being in an
    UNKNOWN state."                       ="The text output from the last service check (i.e. Ping OK)."                       f"This object contains any performance data that may have been returned by
    the last service check."                       ("Table of Nagios service notifications."                       r"Nagios service notifications extends the nagiosSvcEnevtsTable when
    a notification is generated for an event."                       �"A string identifying the type of notification that is being sent
    (PROBLEM, RECOVERY, ACKNOWLEDGEMENT, FLAPPINGSTART or FLAPPINGSTOP)."                      �"The current notification number for the service or host. The notification
    number increases by one (1) each time a new notification is sent out for a
    host or service (except for acknowledgements). The notification number is
    reset to 0 when the host or service recovers (after the recovery
    notification has gone out). Acknowledgements do not cause the notification
    number to increase."           -- Integer32
           �"A string containing the name of the user who acknowledged the service
    problem. This object is only valid in notifications where the
    nSvcNotifyType object is set to ACKNOWLEDGEMENT."                       �"A string containing the acknowledgement comment that was entered by the
    user who acknowledged the service problem.  This object is only valid in
    notifications where the nSvcNotifyType object is set to ACKNOWLEDGEMENT."                       V"The SNMP trap that is generated as a result of an event with the host
    in Nagios."                 j"The SNMP trap that is generated as a result of an event requiring
    notification for a host in Nagios."                 Y"The SNMP trap that is generated as a result of an event with the service
    in Nagios."                 m"The SNMP trap that is generated as a result of an event requiring
    notification for a service in Nagios."                        