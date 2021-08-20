from bs4 import BeautifulSoup
import requests
import datetime
import os
import sched, time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

urlSIMM = ("https://www.medellin.gov.co/simm/mapas/camaras.html")

r = requests.get(urlSIMM)
s = sched.scheduler(time.time, time.sleep)

def _load_Cams(sc):
	
	logging.info('Starting scraper on {}...'.format(urlSIMM))

	html = r.content
	soup = BeautifulSoup(html, 'html.parser')

	cams = []
	onlineCams = soup.find_all(class_="cameraThumb")
	success = 0
	paths = 0
	
	logging.info('Cheking paths...')

	logging.info('Scraper was started!')
	
	for online in onlineCams:
		
		urlCam = online.find('img').get('src')
		cams.append(('{}'.format((urlCam.split('/')[-1]))))
		logging.info('Cam {} found!'.format(urlCam))

		nowFolder = datetime.datetime.now().strftime('%Y_%m_%d')
		nowFile = datetime.datetime.now().strftime('%H:%M:%S')

		for cam in cams:

			#response = requests.get(urlCam)

			camName = (cam.replace('imagen', 'cam'))
			folderName = camName.replace('.jpg','')
			file_name = '{}_{}_{}'.format(nowFolder,nowFile,camName)
			pathDirs = (('{}/{}'.format(folderName,nowFolder)))

			try:
				if not os.path.exists('{}/{}'.format(folderName,nowFolder)):
					os.makedirs('{}/{}'.format(folderName,nowFolder))
				
					logging.info('New path: {} was create.'.format(pathDirs))

				response = requests.get(urlCam)
				success = 0

				if response.status_code == 200:


					if cam in urlCam:
						with open(os.path.join(folderName,nowFolder,file_name), 'wb') as f:
				    			f.write(response.content)
				    			logging.info('Downloading {}'.format(urlCam))
							
						success =+1

						logging.info('{} saved in {} as {} at {}'.format(folderName,file_name,pathDirs,nowFile))

					#s.enter(0, 0, _load_Cams, (sc,))

				#logging.info('{} cam(s) scraped'.format(success))

				#s.enter(0, 0, _load_Cams, (s,))
				#s.run()
				
			except:
				pass

	s.enter(0, 0, _load_Cams, (sc,))

	logging.info('{} cam(s) scraped'.format(success))
	logging.info('{} cam(s) scraped'.format(paths))
s.enter(0, 0, _load_Cams, (s,))
s.run()

if __name__ == '__main__':
	_load_Cams()