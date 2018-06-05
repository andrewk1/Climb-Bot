import praw
import requests
import json
import time 
import re

# Function iterates over each submission title and checks if the title contains route syntax that indicates the post is about a route
def parse_titles(bot, subreddit):
	start_time = time.time()
	for submission in subreddit.stream.submissions():
		if (submission.created_utc < start_time):
			continue		

		title = submission.title
		# regex matches sequence of capitalized words followed by climb grade notation (V or 5.)
		route_regex = '([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+) [( ]?(5.[0-9][0-9]?[A-Za-z]|[Vv][0-9][0-9]?)'
		route_name = re.search(route_regex, title)
		print route_name
		comment = make_get_request(route_name.group(0))
		if comment != 'NA':
			submission.reply(comment)

# Call custom google search engine API to parse the formulated title and gather theCrag's metadata for the route
def make_get_request(route):
	key = 'key=***' 
	cx = 'cx=***' 
	query= 'q='+route
	google_url = 'https://www.googleapis.com/customsearch/v1?' + key + cx + query
	response = requests.get(google_url)
	parsed_response= json.loads(response.text)
	return form_post(parsed_response)

# Extract data from google's JSON response and form a post
def form_post(parsed_response):
	# Check if Google search received a hit
	if parsed_response['searchInformation']['totalResults'] == 0 or 'items' not in parsed_response:
		return 'NA'
	title = parsed_response['items'][0]['title']
	print title
	breadcrumb = parsed_response['items'][0]['pagemap']['breadcrumb']
	count = 0
	# Build up region string
	region_string = ''
	for key in breadcrumb:
		region = breadcrumb[count]['title']
		if (count > 0) :
			region_string = region + ', ' + region_string
		else :
			region_string = region;
		count+=1

	metatags = parsed_response['items'][0]['pagemap']['metatags']
	country = breadcrumb[0]['title']
	latitude = metatags[0]['place:location:latitude']
	longitude = metatags[0]['place:location:longitude']
	google_pin = 'https://www.google.com/maps/@?api=1&map_action=map&basemap=satellite&zoom=19&center=' + latitude + ',' + longitude
	link = metatags[0]['og:url']
	if (' in ' in title):
		title = title[:title.index(' in ')]
	# Truncate values to 3rd decimal place
	lat_decimal = latitude.index('.')
	latitude = latitude[:lat_decimal+4]
	long_decimal = longitude.index('.')	
	longitude = longitude[:long_decimal+4]

	# Format comment response
	return 'I found a route! [' + title + '](' + link + ') in ' + region_string + '\n\nGPS Location: [' + latitude + ', ' + longitude + ']('+google_pin+')' + '\n\n ' + '\n\n^^^I ^^^am ^^^a ^^^bot ^^^| ^^^Data ^^^from ^^^[theCrag.com](https://www.thecrag.com/) ^^^| ^^^Feedback ^^^welcome ^^^at ^^^[r/climbBot](https://www.reddit.com/r/climbBot/)'

if __name__ == "__main__":
	bot = praw.Reddit(
		user_agent='climb-bot posts additional information on climbing routes it finds, created by /u/Akondrich, email: andrewkondrich@gmail.com',
		client_id='***', 
		client_secret='***', 
		username='climb-bot',
		password='***') 
	subreddit = bot.subreddit('climbBot')
	parse_titles(bot, subreddit)

