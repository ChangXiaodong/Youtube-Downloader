#coding=utf-8
import urllib
import urllib2
import sys
import time
import argparse
import os
from urlparse import parse_qs
from urllib2 import URLError

class Youtube(object):
	def request(self, video_url):
		request_url = 'http://www.youtube.com/get_video_info?'
		if 'http://www.youtube.com/watch?v' in parse_qs(video_url).keys(): #生成一个字典  对不同协议网址分类处理 把video_id取出
			request_url += parse_qs(video_url)['http://www.youtube.com/watch?v'][0]
		elif 'https://www.youtube.com/watch?v' in parse_qs(video_url).keys():
			request_url = 'https://www.youtube.com/get_video_info?video_id='+parse_qs(video_url)['https://www.youtube.com/watch?v'][0]
		elif 'v' in parse_qs(video_url).keys():
			request_url += parse_qs(video_url)['v'][0]
		else :
			sys.exit('Error : Invalid Youtube URL Passing %s' % video_url)
		
		# proxy_goagent = urllib2.ProxyHandler({'https': '127.0.0.1:8087'})  #过代理
		# opener = urllib2.build_opener(proxy_goagent)
		# urllib2.install_opener(opener)
		# response = urllib2.urlopen(request_url)
		request = urllib2.Request(request_url)
		try:
			response = urllib2.urlopen(request_url)
			self.video_info = parse_qs(response.read())
			return response
		except URLError:
			sys.exit('Error : Invalid Youtube URL %s' % video_url)
	def read(self):
		global response
		print response.read()
	def get_download_urls(self):
		url_encoded_fmt_stream_map = self.video_info['url_encoded_fmt_stream_map'][0].split(',')
		entrys = [parse_qs(entry) for entry in url_encoded_fmt_stream_map]
		url_maps = [dict(url=entry['url'][0], type=entry['type']) for entry in entrys]
		return url_maps
	def get_write_download_urls(self):
		type = getFileType('mp4')
		video_url_map=self.get_download_urls()
		url = ''

		for entry in video_url_map:
			entry_type = entry['type'][0]
			entry_type = entry_type.split(';')[0]
			if entry_type.lower() == type.lower():
				url = entry['url']
				break
		return url
	def download_video(self):
		type = getFileType('mp4')
		video_url_map=self.get_download_urls()
		video_title=self.get_title()
		url = ''

		for entry in video_url_map:
			entry_type = entry['type'][0]
			entry_type = entry_type.split(';')[0]
			if entry_type.lower() == type.lower():
				url = entry['url']
				break

		if url == '' :
			sys.exit('Error :Sorry,Can not find video\'s url')
			
		#print url
		downloader(url, video_title+'.'+'mp4')

		sys.exit(0)
		
	def get_author(self):
		return self.video_info['author'][0].decode('utf-8')

	def get_watermark(self):
		return self.video_info['watermark'][0].decode('utf-8')

	def get_timestamp(self):
		return self.video_info['timestamp'][0].decode('utf-8')
		
	def get_length_seconds(self):
		return self.video_info['length_seconds'][0].decode('utf-8')
		
	def get_title(self):
		title = self.video_info['title'][0].decode('utf-8')
		return title

		
	def get_hl(self):
		return self.video_info['hl'][0].decode('utf-8')
	
	def get_view_count(self):
		return self.video_info['view_count'][0].decode('utf-8')
	
	def get_video_verticals(self):
		return self.video_info['video_verticals'][0].decode('utf-8')
	
	def get_video_id(self):
		return self.video_info['video_id'][0].decode('utf-8')
		
def getFileType(extension):
	if extension.lower() == 'webm':
		return 'video/webm'
	if extension.lower() == 'mp4':
		return 'video/mp4'
	if extension.lower() == '3gp':
		return 'video/3gpp'
	if extension.lower() == 'flv':
		return 'video/x-flv'
	return None

def downloader(url, filename, prefix_message='^_^'):
	"""
	download file from url
	"""
	if os.path.exists(filename):
		os.remove(filename)
		#sys.exit('Error : file already exists')
		
	# proxy_goagent = urllib2.ProxyHandler({'https': '127.0.0.1:8087'})  #过代理
	# opener = urllib2.build_opener(proxy_goagent)
	# urllib2.install_opener(opener)
	#link = urllib2.urlopen(url)
	request=urllib2.Request(url)
	link = urllib2.urlopen(request)
	
	file=open(filename, 'wb')
	meta=link.info()
	filesize=float(meta.getheader('Content-Length'))
	size_message = 'Wow!Your downloading file size is %.2f M\n' %(filesize/1024/1024)
	
	buff_size=16384
	downloaded_size=0

	sys.stdout.write(prefix_message+'\n'+size_message+'\n')
	sys.stdout.flush()
	
	while True:
		buffer = link.read(buff_size)
		if not buffer:
			break
		downloaded_size += len(buffer)
		file.write(buffer)
		display = '%s ------------ %d / %d' %(filename, downloaded_size, filesize)
		sys.stdout.write("\r"+display)
		sys.stdout.flush()

	time.sleep(1)
	sys.stdout.write('\n')
	sys.stdout.flush()
	sys.stdout.write('Downloading Complete!\nEnjoy!')
	sys.stdout.flush()
	file.close()
def main():
	youtube = Youtube()
	request=youtube.request("https://www.youtube.com/watch?v=BEG-ly9tQGk")
	youtube.download_video()

if __name__ == '__main__':
     main()


#youtube = Youtube()
#request = youtube.request("https://www.youtube.com/watch?v=beg-ly9tqgk")
#video_url_map = youtube.get_download_urls()
#video_title = youtube.get_title()
#print video_url_map
#print video_title