import tweepy #https://github.com/tweepy/tweepy
import csv
import html
import credentials
import Dostoevsky

def clear_word(word):
	word = re.sub(r'[^\-\W]',r'',word)
	return word

class Listener(tweepy.StreamListener):
	
	def on_status(self, status):
		if status.user.screen_name != "FarGalaxyBot":
			print('Reply to user @{}, tweet: {}'.format(status.user.screen_name, status.text))
			last_word = clear_word(status.text.split()[-1].lower())
			answer = Dostoevsky.generate_answer(last_word)
			if len(answer) < 220:
				api.update_status('@{} {} https://twitter.com/{}/status/{}'.format(
						status.user.screen_name, 
						answer,
						status.user.screen_name,
						status.id
					), 
							in_reply_to_status_id=status.id)
	
	
	def on_error(self, status_code):
		if status_code == 420:
			# если окажется, что мы посылаем слишком много запросов, то отсоединяемся
			return False
		# если какая-то другая ошибка, постараемся слушать поток дальше
		return True

#Twitter API credentials
consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_key = credentials.access_token
access_secret = credentials.access_token_secret


def work():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	Listener = Listener()
	myStream = tweepy.Stream(auth = api.auth, listener=Listener)

	myStream.filter(track=['@dostoevsky_bot'])

if __name__ == '__main__':
	work()