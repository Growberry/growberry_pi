import json
import cPickle as pickle
shelve




#boot:

#pull in config
    # growing or not
        #if growing - start growing
        #if not - idle, but keep checking the config for a change in grow-status

    # online or not
        #if online - 1. flip
    # load grow settings
    #





#######################################################################
###########                     CONFIG                  ###############
#######################################################################

{
    'GROWING': True,
    'ONLINE': True,
    'SETTINGS':{
        'startdate':'date'
    }





}






#
import json
with open('data.json', 'w') as fp:
    json.dump(data, fp)