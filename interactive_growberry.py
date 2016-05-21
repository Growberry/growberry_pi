from configparser import ConfigParser

if __name__ == "__main__":
    cfg = ConfigParser()
    ### *** WRITE config file ***
    """
    cfg['configData1'] = {'conf1': 'one', 'conf2': '12', 'conf3': 'false'}
    cfg['configData2'] = {}
    cfg['configData2']['config_string'] = 'string'  # set "string"
    cfg['configData2']['config_bool'] = 'true'  # set "bool"
    cfg['configData2']['config_int'] = '21'     # set "int"
    cfg['configData2']['config_float'] = '10.211'   # set "float"

    with open('config.ini', 'w') as configfile:
        cfg.write(configfile)
    """

    ### *** READ config file ***
    cfg.read('config.ini')
    print(cfg.sections())       # return all sections
    print(cfg.items('configData1')) # return section's list
    print(cfg.get('configData1', 'conf1'))
    print(cfg.get('configData1', 'conf2'))
    print(cfg.get('configData1', 'conf3'))

    print(cfg.get('configData2', 'config_string'))  # get "string" object
    print(cfg.getboolean('configData2', 'config_bool')) # get "bool" object
    print(cfg.getint('configData2', 'config_int'))      # get "int" object
    print(cfg.getfloat('configData2', 'config_float'))  # get "float" object