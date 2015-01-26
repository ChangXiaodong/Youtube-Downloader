import Youtube
import os
def main():
	youtube = Youtube.Youtube()
	url = raw_input('Please input Youtube URL: \n')
	request=youtube.request(url)

	author = youtube.get_author()
	watermark = youtube.get_watermark()
	timestamp = youtube.get_timestamp()
	length_seconds = youtube.get_length_seconds()
	title = youtube.get_title()
	hl = youtube.get_hl()
	view_count = youtube.get_view_count()
	video_verticals = youtube.get_video_verticals()
	video_id = youtube.get_video_id()
	download_url = youtube.get_write_download_urls()
	filename = 'Video_info.txt'
	if os.path.exists(filename):
		os.remove(filename)
	file=open(filename, 'w')
	file.write('title:'+title+'\n\n')
	file.write('author:'+author+'\n\n')
	file.write('video_id:'+video_id+'\n\n')
	file.write('length_seconds:'+length_seconds+'s\n\n')
	file.write('download_url:'+download_url+'\n\n')
	file.write('view_count:'+view_count+'\n\n')
	file.write('timestamp:'+timestamp+'\n\n')
	file.write('hl:'+hl+'\n\n')
	file.write('video_verticals:'+video_verticals+'\n\n')
	file.write('video_id:'+video_id+'\n\n')
	file.write('watermark:'+watermark+'\n\n')
	file.close()
	youtube.download_video()

if __name__ == '__main__':
	main()
