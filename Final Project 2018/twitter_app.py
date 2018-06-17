import tweepy #https://github.com/tweepy/tweepy
import csv
import html
import re
import credentials
import Dostoevsky

from time import sleep

#Twitter API credentials
consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_key = credentials.access_token
access_secret = credentials.access_token_secret

def clear_word(word):
	word = re.sub(r'[^\-\w]',r'',word)
	return word

class Listener(tweepy.StreamListener):
	
	def on_status(self, status):
		print('Caught signal to start')
		if status.user.screen_name != "DostoevskyBot":
			print('Reply to user @{}, tweet: {}'.format(status.user.screen_name, status.text))
			last_word = clear_word(str(status.text).split()[-1].lower())
			print('Word derived as',last_word)
			try:
				answer = Dostoevsky.generate_answer(last_word)
			except:
				answer = 'Извините, кажется, Достоевскому нечего вам ответить!'
			answer = re.sub(r'\n',' ',answer)
			splitted_answer = answer.split(' ')
			i = 0
			I = 0
			response = ""
			while len(answer) > 239:
				if i == 0:
					response_length = len(splitted_answer[i])
				else:
					response = '…'
					response_length = len(splitted_answer[i])+len('…')
				while response_length < 240:
					I += 1
					response_length += len(' ') + len(splitted_answer[I]) + len('…')
				for k in range(i,I):
					response += ' '+splitted_answer[k]
				i = I
				response += '…'
				status = api.update_status('@{} {} https://twitter.com/{}/status/{}'.format(
						status.user.screen_name, 
						response,
						status.user.screen_name,
						status.id
					), 
							in_reply_to_status_id=status.id)
				answer = answer[len(response):]
			
			if i>0:
				response = '…'
			response += answer
			status = api.update_status('@{} {} https://twitter.com/{}/status/{}'.format(
					status.user.screen_name, 
					response,
					status.user.screen_name,
					status.id
				), 
						in_reply_to_status_id=status.id)
	
	
	def on_error(self, status_code):
		print('Caught error',status_code)
		if status_code == 420:
			# если окажется, что мы посылаем слишком много запросов, то отсоединяемся
			sleep(900)
			return False
		# если какая-то другая ошибка, постараемся слушать поток дальше
		return True


if __name__ == '__main__':
	while True:
		try:
			auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_key, access_secret)
			api = tweepy.API(auth)
			myListener = Listener()
			myStream = tweepy.Stream(auth = api.auth, listener=myListener)

			myStream.filter(track=['@DostoevskyBot', '@dostoevskyBot', '@dostoevskybot', '@Dostoevskybot'])
		except:
			pass