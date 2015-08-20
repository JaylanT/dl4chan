#! python3
# dl4Chan.py - Downloads all images on 4Chan post
# Usage: py dl4chan.py <folder> <4chan URL>

import requests, os, bs4, sys, re, time

def updateTime():
	"""Returns the current time"""
	
	newTime = '[' + time.strftime("%H:%M:%S") + '] '
	return newTime

def downloadImg(newFileName, imgURL, imgURLBasename):
	"""Downloads the image to the folder

	Keyword arguments:
	newFileName -- the path to folder and file name
	imgURL -- the URL of the image"""

	res = requests.get(imgURL)
	res.raise_for_status()
	
	print(updateTime() + 'Downloading IMAGE %s...' % (imgURLBasename))
	imageFile = open(newFileName, 'wb')
	for chunk in res.iter_content(1000000):
		imageFile.write(chunk)
	imageFile.close()
	visitedImgUrl.append(imgURL)

def downloadPage(newFolder, url):
	"""Downloads and parses the HTML page.
	Continually check for updates on page every 60s.

	Keyword arguments:
	newFolder -- the folder to contain images
	url -- the url of HTML page"""

	while True:
		try:
			print(updateTime() + 'Downloading PAGE %s...' % url)
			res = requests.get(url)
			res.raise_for_status()

			soup = bs4.BeautifulSoup(res.text, "html.parser")
			postElem = soup.find_all('div', class_='fileText')

			if postElem:
				for post in postElem:
					imgURL = "http:" + post.a['href']
					imgURLBasename = os.path.basename(imgURL)
					newFileName = os.path.join(newFolder, imgURLBasename)

					if not os.path.isfile(newFileName):
						downloadImg(newFileName, imgURL, imgURLBasename)
					else:
						print(updateTime() + 
							'Skipping copied IMAGE %s...' % (imgURLBasename))
			else:
				print("No images were found.")		

			print('Will check again in 60s (Press Ctrl+C to cancel)')
			time.sleep(60)
		except KeyboardInterrupt:
			print('Done and exiting.')
			exit()

def isFolderNameValid(name):
	"""Checks if the folder name is valid

	Keyword arguments:
	name -- the folder name"""

	folderScan = re.compile('^[^\\/?%*:|"<>\.]+$')
	try:
		if not folderScan.search(name):
			raise NameError()
	except NameError:
		print("Name Error:\nA file name can't contain any of the following characters: < > : \" / \\ | ? * ")
		exit()

def main():
	"""Starts downloading page after checking
	if the folder name and URL is present and valid."""

	try:
		newFolder = sys.argv[1]
		url = sys.argv[2]

		isFolderNameValid(newFolder)
		os.makedirs(newFolder, exist_ok=True)
	except IndexError:
		print("Index Error:\nUsage- dl4chan.py <folder> <URL> - missing folder or URL")
		exit()

	downloadPage(newFolder, url)
	print('Done.')

visitedImgUrl = []

if __name__ == "__main__": main()
