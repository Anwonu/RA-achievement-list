import configparser

def validateConfig():
	default = {
		'API': {
			'key': '',
			'readonly': False
		},
		'User': {
			'username': '',
			'readonly': False
		},
		'Initial config': {
			'posX': 50,
			'posY': 50,
			'game_id': 0,
			'bg_color': 'magenta',
			'size': 1,
		},
		'Timer': {
			'width': 300,
			'height': 300,
			'posX': 50,
			'posY': 50,
			'timer_color': 'green',
			'opened': False
		},
		'Achievement list 1': {
			'width': 680,
			'height': 680,
			'posX': 50,
			'posY': 50,
			'size': 1,
			'show_unlocked': True,
			'show_locked': True
		},
	}
	config = configparser.ConfigParser()
	config.read('config.ini')

	for s in default:
		if not s in config:
			config.add_section(s)
			config[s] = default[s]
		else:
			for f in default[s]:
				if f not in config[s]:
					config.set(s, f, str(default[s][f]))

	with open('config.ini', 'w') as configfile:
		config.write(configfile)

def getConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config

def getConfigSection(section):
	config = configparser.ConfigParser()
	config.read('config.ini')
	if section in config:
		return config[section]
	return None

def getConfigField(section, field):
	config = configparser.ConfigParser()
	config.read('config.ini')
	if section in config and field in config[section]:
		return config[section][field]
	return None

def updateConfig(section, field, value):
	config = configparser.ConfigParser()
	config.read('config.ini')

	if not section in config:
		config.add_section(section)
	config.set(section, field, str(value))

	with open('config.ini', 'w') as configfile:
		config.write(configfile)

def updateConfigSection(section, values):
	config = configparser.ConfigParser()
	config.read('config.ini')

	if not section in config:
		config.add_section(section)
	for item in values:
		config.set(section, item, str(values[item]))

	with open('config.ini', 'w') as configfile:
		config.write(configfile)