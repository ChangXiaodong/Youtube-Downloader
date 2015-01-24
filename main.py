#coding=utf-8
import urllib
import urllib2
import sys
import time
import argparse
from os import path
from urlparse import parse_qs
from urllib2 import URLError

class YoutubeGetInfo(object):
	def request(self, video_url):
		request_url = 'http://www.youtube.com/get_video_info?video_id='
		#print parse_qs(video_url).keys()
		if 'http://www.youtube.com/watch?v' in parse_qs(video_url).keys(): #生成一个字典  对不同协议网址分类处理
			 request_url += parse_qs(video_url)['http://www.youtube.com/watch?v'][0]
		elif 'https://www.youtube.com/watch?v' in parse_qs(video_url).keys():
			 request_url = 'https://www.youtube.com/get_video_info?video_id='+parse_qs(video_url)['https://www.youtube.com/watch?v'][0]
		elif 'v' in parse_qs(video_url).keys():
			 request_url += parse_qs(video_url)['v'][0]
		else :
			 sys.exit('Error : Invalid Youtube URL Passing %s' % video_url)
		try:
			proxy_goagent = urllib2.ProxyHandler({'https': '127.0.0.1:8087'})  #过代理
			opener = urllib2.build_opener(proxy_goagent)
			urllib2.install_opener(opener)
			response = urllib2.urlopen(request_url)
			self.video_info = parse_qs(response.read())
		except URLError:
			sys.exit('Error : Invalid Youtube URL Passing %s' % video_url)

def get_title(videoinfo):
	title = videoinfo.video_info['title'][0].decode('utf-8')
	return title

def get_download_urls(videoinfo):
	
	url_encoded_fmt_stream_map = videoinfo.video_info['url_encoded_fmt_stream_map'][0].split(',')
	entrys = [parse_qs(entry) for entry in url_encoded_fmt_stream_map]
	url_maps = [dict(url=entry['url'][0], type=entry['type']) for entry in entrys]
	return url_maps

    
def downloader(url, filename, prefix_message=''):
	if path.exists(filename):
		sys.exit('Error : file already exists')

	request=urllib2.Request(url)
	file=open(filename, 'wb')
	link=urllib2.urlopen(request)
	meta=link.info()
	filesize=int(meta.getheader('Content-Length'))
	size_message = 'downloading file size is %d byte\n' %(filesize)

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
		display = '%s .............. %d / %d' %(filename, downloaded_size, filesize)
		sys.stdout.write("\r"+display)
		sys.stdout.flush()

	time.sleep(1)
	sys.stdout.write('\n')
	sys.stdout.flush()
	file.close()

    
#def main():

    #parser = argparse.ArgumentParser(description='YoutubeVideoDownload -- a small and simple program for downloading Youtube Video File')
    #parser.add_argument('url', metavar='url', type=str, help='Youtube video URL string with "http://" prefixed')
    #parser.add_argument('type', metavar='type', type=str, help="Downloaded file's type ( webm || mp4 || 3gp || flv)")
    #argvs = parser.parse_args()
    #url_str = argvs.url
    #type = __getFileType(argvs.type)
    
    #if not type:
        #sys.exit('Error : Unsupported file type %s' % argvs.type)

    #video_info = VideoInfo(url_str)
    #video_url_map = video_file_urls(video_info)
    #video_title = title(video_info)
    #url = ''

    #for entry in video_url_map:
        #entry_type = entry['type'][0]
        #entry_type = entry_type.split(';')[0]
        #if entry_type.lower() == type.lower():
            #url = entry['url']
            #break

    #if url == '' :
        #sys.exit('Error : Can not find video file\'s url')
    
    #downloader(url, video_title+'.'+argvs.type)
    
    #sys.exit(0)



#if __name__ == '__main__':
    #main()
youtube = YoutubeGetInfo();
video_all_info = youtube.request("https://www.youtube.com/watch?v=RZTei7UMTPk")
video_url_map = get_download_urls(youtube)
video_title = get_title(youtube)
url = ''
#for entry in video_url_map:
	#entry_type = entry['type'][0]
	#entry_type = entry_type.split(';')[0]
	#if entry_type.lower() == type.lower():
		#url = entry['url']
		#break

print youtube.__dict__
print video_url_map