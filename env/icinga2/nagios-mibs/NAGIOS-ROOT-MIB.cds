     �"A string identifying the type of notification that is being sent 
    (PROBLEM, RECOVERY, ACKNOWLEDGEMENT, FLAPPINGSTART or FLAPPINGSTOP).
    "               r"A number that corresponds to the current state of the service: 0=OK, 
    1=WARNING, 2=CRITICAL, 3=UNKNOWN.
    "               _"A number that corresponds to the current state of the host: 0=UP, 1=DOWN, 
    2=UNREACHABLE."              $"A string indicating the state type for the current host check (HARD or 
    SOFT). Soft states occur when host checks return a non-OK (non-UP) state 
    and are in the process of being retried. Hard states result when host 
    checks have been checked a specified maximum number of times."                                         "Objects for Nagios(tm) NMS" �" Subhendu Ghosh
      
      Telephone: +1 201 232 2851
      Email: sghosh@users.sourceforge.net

      Nagios Information:
        http://www.nagios.org
      " "200503090000Z" "200501200000Z" "Spell check" "Initial Version"       -- March 9, 2005
          