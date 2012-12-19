from ConfigParser import SafeConfigParser

if __name__ == "__main__":
	conffile = configos.getenv('HOME')+os.sep+'.cphvb'+os.sep+'config.ini'
	confparser = SafeConfigParser()     # Parser to modify the cphvb configuration file.
	confparser.read(conffile)             # Read current configuration
	confparser.set("node", "children", "simple")  
	confparser.write(open(conffile, 'wb'))
