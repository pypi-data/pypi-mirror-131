
import json

# save info from common.print_info()
last_info = None

# streams为有序list，清晰度高->低排序
def output(video_extractor, pretty_print=True):
    ve = video_extractor
    out = {}
    out['url'] = ve.url
    out['title'] = ve.title
    out['site'] = ve.name
    out['streams'] = []

    try:
        out['streams'].extend(ve.streams_sorted)
    except AttributeError:
        out['streams'].extend(ve.streams.values())

    try:  # 对dash_streams排序
        if ve.dash_streams:
            try:
                out['streams'].extend(
                    [dict([('id', stream_type['id'])] + list(ve.dash_streams[stream_type['id']].items())) for
                     stream_type in ve.__class__.stream_types if stream_type['id'] in ve.dash_streams])
            except:
                out['streams'].extend(
                    [dict([('itag', stream_type['itag'])] + list(ve.dash_streams[stream_type['itag']].items()))
                     for stream_type in ve.__class__.stream_types if stream_type['itag'] in ve.dash_streams])
    except AttributeError:
        pass

    try:
        if ve.audiolang:
            out['audiolang'] = ve.audiolang
    except AttributeError:
        pass
    extra = {}
    if getattr(ve, 'referer', None) is not None:
        extra["referer"] = ve.referer
    if getattr(ve, 'ua', None) is not None:
        extra["ua"] = ve.ua
    if extra:
        out["extra"] = extra
    if pretty_print:
        print(json.dumps(out, indent=4, ensure_ascii=False))
    else:
        print(json.dumps(out))

# a fake VideoExtractor object to save info
class VideoExtractor(object):
    pass

def print_info(site_info=None, title=None, type=None, size=None):
    global last_info
    # create a VideoExtractor and save info for download_urls()
    ve = VideoExtractor()
    last_info = ve
    ve.name = site_info
    ve.title = title
    ve.url = None

def download_urls(urls=None, title=None, ext=None, total_size=None, refer=None):
    ve = last_info
    if not ve:
        ve = VideoExtractor()
        ve.name = ''
        ve.url = urls
        ve.title=title
    # save download info in streams
    stream = {}
    stream['container'] = ext
    stream['size'] = total_size
    stream['src'] = urls
    if refer:
        stream['refer'] = refer
    stream['video_profile'] = '__default__'
    ve.streams = {}
    ve.streams['__default__'] = stream
    output(ve)
