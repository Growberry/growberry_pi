#!/bin/bash
logo="$(tput setaf 2)

 ooooosyhd                         ddddddddddd    
 ooooooooooy           dddddddddddddddddddddd     
 yooooooooooo      ddddddddddddddddddddddddd      
  hoooooooooos   ddddddddddddddddddddddddd        
      ddhhhyso  dddddddddddddddddddddddd          
             dhdddddddddddddddddddddd             
              dddddddddddd                        
              ddddddd                             
              dddd.                                $(tput setaf 2)
              ddd.$(tput setaf 1)        ddhhhhhhhhhhhhhhhh$(tput setaf 2)
             /dd.$(tput setaf 1)d    hhhhhhhhhhhhhhhhhhhhhhh$(tput setaf 2)
             dh.$(tput setaf 1)hd   hhhy/-:shhhhhhhhhhhhhhhhh$(tput setaf 2)
             d.$(tput setaf 1)hhd   hhh-   *hhhhhhhhhhhhhhhhh$(tput setaf 2)
             .$(tput setaf 1)hhhd   hhhy/:/shhhhhhhhhhhhhhhhh    
             hhhhd   hhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhd   ddddddddddddddddddhhhhhhh    
             hhhhd                     hhhhhhh    
             hhhhd                     hhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    
             hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhd     
               ddhhhhhhhhhhhhhhhhhhhhhhhdd        

$(tput sgr0)"
if [ `whoami` != "root" ]; then
  echo "$logo"
  echo "Run as sudo to update your motd."
else
  echo "$logo" > /etc/motd
  /etc/init.d/bootlogs
  echo "Updated MOTD. Log in again to see the new logo."
fi
