from ConfigParser import SafeConfigParser

if __name__ == "__main__":
	conffile = os.getenv('HOME')+os.sep+'.bohrium'+os.sep+'config.ini'
	confparser = SafeConfigParser()     # Parser to modify the Bohrium configuration file.
	confparser.read(conffile)             # Read current configuration
	confparser.set("node", "children", "simple")  
	confparser.write(open(conffile, 'wb'))
