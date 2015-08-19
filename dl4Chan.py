#! python3
# dl4Chan.py - Downloads all images on 4Chan post
# Usage: py dl4chan.py <folder> <4chan URL>

import requests, os, bs4, sys, re

def isFolderNameValid(name):
	folderScan = re.compile('^[^\\/?%*:|"<>\.]+$')
	try:
		if not folderScan.search(name):
			raise NameError()
	except NameError:
		print("Name Error: \nA file name can't contain any of the following characters: < > : \" / \\ | ? * ")
		exit()

# Take link from cmd line
try:
	newFolder = sys.argv[1]
	url = sys.argv[2]

	isFolderNameValid(newFolder)

	os.makedirs(newFolder, exist_ok=True)
except IndexError:
	print("Usage: dl4chan.py <folder> <URL> - missing folder or URL")
	sys.exit(1)

# Download and then parse the page
print('Downloading PAGE %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")

postElem = soup.find_all('div', class_='fileText')

if not postElem:
	print("No images were found.")
else:
	for post in postElem:
		imgURL = "http:" + post.a['href']

		# Download img to computer
		print('Downloading IMAGE %s...' % (imgURL))
		res = requests.get(imgURL)
		res.raise_for_status()
		newFileName = os.path.join(newFolder, os.path.basename(imgURL))
		if not os.path.isfile(newFileName):
			imageFile = open(newFileName, 'wb')
			for chunk in res.iter_content(1000000):
				imageFile.write(chunk)
			imageFile.close()
		else:
			print('Duplicate file, skipping.')

print('Done.')

# argv[2] could be pyperclip.paste() if missing from cmd line
# make it scrape every few minutes
# print timestamp alongside downloading image
# url parse and only say the basename when dlin page