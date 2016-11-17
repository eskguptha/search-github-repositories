import threading
import requests
import getopt, sys
import json
import pprint
import pandas as pd

git_output = []

def crawl(*args,**kwargs):
	# args -- thread no, kwargs -- query input parameters  
	url = "https://api.github.com/search/repositories?per_page=100&page=%s"%args[0]
	# Getting response from github api based on query args
	git_result =  requests.get(url, params=kwargs)
	if git_result:
		git_data =  json.loads(git_result.text)
		try:
			# saving git response items into an array like list
			git_output.extend(git_data['items'])
		except KeyError:
			pass
	return None

def main(input_params):
	print "######### Process Started #########"
	threads = []
	# Creating Five threads and assigning task to each thread
	for i in range(1,6):
		# Creating new thread and assing task
		thread = threading.Thread(target=crawl,args=[i],kwargs=input_params)
		thread.start()
		threads.append(thread)

	#blocks the thread in which you're making the call, until thread1 is finished.
	for thread in threads:
		thread.join()
	
	# results from all threads & combined aggregated results
	if git_output:
		# loading result into pandas dataframe
		df = pd.DataFrame(git_output)
		# Aggregation based on below columns using pandas
		grouped = df.groupby(['archive_url','watchers_count','forks_count']).agg(sum)
		grouped_result =  grouped.reset_index().to_dict('records')
		# A pretty printed list of results using pprint with indent level 4
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(grouped_result)
	print "######### Process Finished #########"
	return None



if __name__ == "__main__":
	try:
		# Checking Input Arguments
		params, args = getopt.getopt(sys.argv[1:], "ho:v", ["q=","sort=","order="])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	params = dict(params)
	# Compare input arguments
	if all (k in params.keys() for k in ('--q','--sort','--order')):
		input_params = {"q":params['--q'], "sort":params['--sort'], "order":params['--order']}
		main(input_params)
	else:
		print "Invalid Arguments / argument missing"
		print "Ex: python github.com.py --q=ninja+language:python --sort=stars --order=asc"
