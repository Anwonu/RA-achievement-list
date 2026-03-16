import requests
from pprint import pprint
from config import *
from alerts import *
import constants as ct


# add '&' at the start of params, please
def api(url, params):
	key = getConfigField('API', 'key')
	url = ct.api_url + url + '?y=' + key + params

	if key:
		try:
			# Make a GET request to the API endpoint using requests.get()
			response = requests.get(url)

			# Check if the request was successful (status code 200)
			if response.status_code == 200:
				answer = response.json()
				return answer
			else:
				json = response.json()

				match response.status_code:
					case 401:
						showError('Error 401', "Unauthenticated; maybe try copy/pasting your API key again.")
					case 404:
						showWarning('Error 404', "User not found.")
					case 422:
						showWarning('Error 422', "Username/ULID can only contain letters and numbers.")
					case _:
						pprint(json)
						showError('Error ' + str(response.status_code), json['message'])
				return None
		except requests.exceptions.RequestException as e:
			print('Error:', e)
			return None

def getProfile(user, params=''):
	return api('API_GetUserProfile.php', '&u=' + user + params)

def getRecent(mins, params=''):
	username = getConfigField('User', 'username')
	return api('API_GetUserRecentAchievements.php', '&u=' + username + '&m=' + str(mins) + params)

def getGameExtended(game_id, params=''):
	return api('API_GetGameExtended.php', '&i=' + str(game_id) + params)

def getGameWithUser(game_id, params=''):
	username = getConfigField('User', 'username')
	return api("API_GetGameInfoAndUserProgress.php", "&u=" + username + "&g=" + game_id)