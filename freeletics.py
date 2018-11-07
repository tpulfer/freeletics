import requests
import json

url_login = 'https://api.freeletics.com/user/v1/auth/password/login'
url_feed = 'https://api.freeletics.com/v3/users/4155941/feed_entries?page='

workout_count = {}
exercise_count = {}
i = 1

login_payload = {	"login": {
		"email": "youremailhere",
		"password": "yourpwhere"
	}
}

login_response = requests.post(url_login, json=login_payload)
login_ans = json.loads(login_response.text)
id_token = login_ans["auth"]["id_token"]
header = {'Authorization': 'Bearer '+id_token}

while len(requests.get(url_feed+str(i), headers=header).text) > 30:
#while i < 2:
	feed_entries = requests.get(url_feed+str(i), headers=header)
	feed_ans = json.loads(feed_entries.text)
	for workout in feed_ans["feed_entries"]:
		#print(workout)
		if workout["object"]["workout"]["title"] in workout_count:
			workout_count.update({workout["object"]["workout"]["title"]: workout_count[workout["object"]["workout"]["title"]] + 1})
		else:
			workout_count.update({workout["object"]["workout"]["title"]: 1})
		for round in workout["object"]["workout"]["rounds"]:
			for exercise in round:
				if "exercise_slug" in exercise and isinstance(exercise["quantity"], int):
					if exercise["exercise_slug"] in exercise_count:
						exercise_count.update({exercise["exercise_slug"]: exercise_count[exercise["exercise_slug"]] + exercise["quantity"]})
					else:
						exercise_count.update({exercise["exercise_slug"]: exercise["quantity"]})
		    
	i = i + 1

for keys,values in workout_count.items():
    print(keys, ': ', values)

print('---------------')

for keys,values in exercise_count.items():
    print(keys, ': ', values)




