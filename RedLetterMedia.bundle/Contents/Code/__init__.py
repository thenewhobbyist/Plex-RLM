TITLE = 'Red Letter Media'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFIX = '/video/redlettermedia'
NS = {'blip':'http://blip.tv/dtd/blip/1.0',
            'media':'http://search.yahoo.com/mrss/'}

RSS_FEED = 'http://redlettermedia.blip.tv/rss'
PLINKETT = 'http://www.redlettermedia.com/plinkett/'
PLINKETTCATS = 'star-trek', 'star-wars', 'other-movies', 'commentary-tracks', 'plinkett-review-trailers', 'plinkett-review-extras', 'mr-plinkett-the-animated-series'
BOW = 'http://redlettermedia.com/best-of-the-worst/'
HITB = 'http://redlettermedia.com/half-in-the-bag/%s'
HITBMORE = '2011-episodes', '2012-episodes', '2013-episodes'

MAX_EPISODES_PER_PAGE = 10

###################################################################################################

# Set up containers for all possible objects
def Start():

  ObjectContainer.title1 = TITLE

###################################################################################################
@handler('/video/redlettermedia', TITLE, art=ART, thumb=ICON)
def Mainmenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(PlinkMenu, title="Mr. Plinkett"), title="Mr. Plinkett", thumb = R(ICON)))
    oc.add(DirectoryObject(key=Callback(HalfBag, title="Half in the Bag"), title="Half in the Bag", thumb = R(ICON)))
    oc.add(DirectoryObject(key=Callback(BestWorst, title="Best of the Worst"), title="Best of the Worst", thumb = R(ICON)))
    oc.add(DirectoryObject(key=Callback(AllShows, title="All Shows"), title="All Shows", thumb = R(ICON)))
    return oc

###################################################################################################
# Submenu for Plinkett
@route(PREFIX + '/plinkett/plinkmenu')
def PlinkMenu(title):
	oc = ObjectContainer(title2=title)
	oc.add(DirectoryObject(key=Callback(StarTrek, title='Star Trek'), title='Star Trek', thumb = R(ICON)))
	oc.add(DirectoryObject(key=Callback(StarWars, title='Star Wars'), title='Star Wars', thumb = R(ICON)))
	oc.add(DirectoryObject(key=Callback(OtherMovies, title='Other Movies'), title='Other Movies', thumb = R(ICON)))
	#oc.add(DirectoryObject(key=Callback(Commentary, title='Commentary', sort_type='commentary'), title='Commentary', thumb = R(ICON)))
	#oc.add(DirectoryObject(key=Callback(Trailers, title='Trailers', sort_type='Trailers'), title='Trailers', thumb = R(ICON)))
	#oc.add(DirectoryObject(key=Callback(Extras, title='Extras', sort_type='extras'), title='Extras', thumb = R(ICON)))
	return oc

###################################################################################################
@route(PREFIX + '/plinkett')
def Plinkett(title):
	oc = ObjectContainer(title=title2)
	for category in PLINKETTCATS:
		link = PLINKETT + category
		for vidlink in HTML.ElementFromURL(link).xpath('//*[@class="post clearfix"]/div/p/a'):
			if vidlink[0:4] != 'http':
				vidlink = PLINKETT + vidlink
			Log('Video URL is %s' %vidlink)
			url = HTML.ElementFromURL(link).xpath('//embed')
			Log('Video is %s' %video)
			thumb = HTML.ElementFromURL(link).xpath('//*[@class="post clearfix"]/div/p/a/img')[0]
			Log('Thumbnail is %s' %thumb)
			oc.add(VideoClipObject(url = url, thumb = thumb))
	return oc
###################################################################################################
# Star Trek Section of Plinkett reviews.
@route(PREFIX + '/startrek')
def StarTrek(title):
	oc = ObjectContainer(title2=title)

	thumblist = HTML.ElementFromURL(PLINKETT + 'star-trek').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
        nextthumb = 0
	
	# Get list of videos.
	for link in HTML.ElementFromURL(PLINKETT + 'star-trek').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
		Log('Link is %s' %link)
		thumb = thumblist[nextthumb]
		nextthumb = nextthumb + 1
		Log('Thumbnail is %s' %thumb)
		# Some links need the base URL added.
		if link[0:4] != 'http':
	    		link = PLINKETT + link
        	Log('Full link is %s' %link)
	    	try:
			url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
			if url.startswith('http://a.'):
				url = 'http://blip.tv/play/%s.html' % (url[25:36])
	    	except IndexError:
			Log('End of list.')	
		Log('Video is %s' %url)
	    	oc.add(VideoClipObject(url = url, thumb = thumb))
	return oc
###################################################################################################
# Star Wars Section of Plinkett reviews.
@route(PREFIX + '/starwars')
def StarWars(title):
	oc = ObjectContainer(title2=title)
	
	thumblist = HTML.ElementFromURL(PLINKETT + 'star-wars').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
        nextthumb = 0

	# Get list of videos.
	for link in HTML.ElementFromURL(PLINKETT + 'star-wars').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
		Log('Link is %s' %link)
		thumb = thumblist[nextthumb]
                nextthumb = nextthumb + 1
                Log('Thumbnail is %s' %thumb)
	    	# Some links need the base URL added.
	    	if link[0:4] != 'http': 
	    		link = PLINKETT + link
            	Log('Full link is %s' %link)
		try:
	    		url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
			if url.startswith('http://a.'):
                                url = 'http://blip.tv/play/%s.html' % (url[25:36])
                except IndexError:
                        Log('End of list.')
                Log('Video is %s' %url)
	    	oc.add(VideoClipObject(url = url, thumb = thumb))
	return oc	
###################################################################################################
# Other Movies Section of Plinkett reviews.
@route(PREFIX + '/othermovies')
def OtherMovies(title):
	oc = ObjectContainer(title2=title)
	# Get list of videos.
	for link in HTML.ElementFromURL(PLINKETT + 'other-movies').xpath('//*[@class="post clearfix"]/div/p/a'):
		Log('Link is %s' %link)
	    # Some links need the base URL added.
	    	if link[0:4] != 'http': 
	    		link = PLINKETT + link
            	Log('Full link is %s' %link)
	    	url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
	    	Log('Video is %s' %video)
	    	thumb = HTML.ElementFromURL(PLINKETT + 'other-movies').xpath('//*[@class="post clearfix"]/div/p/a/img')
	    	Log('Thumbnail is %s' %thumb)
	    	oc.add(VideoClipObject(url = url, thumb = thumb))
	return oc	
###################################################################################################
# @route('/video/redlettermedia/plinkett', offset = int)
# def Plinkett(title, offset = 0):
    # oc = ObjectContainer(title2=title) #, user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')

    # counter = 0

    # # First we find the list of videos.
    # for link in HTML.ElementFromURL(PLINKETT).xpath('//*[@id="post-main-37"]/div/p/a/@href'):
        # # Some links don't start with the base URL, so we have to add it to them.
        # counter = counter + 1
        # if counter <= offset:
          # continue
        # # Log('link is %s' %link)
        # if link[0:4] != 'http': link = PLINKETT + link
        # Log('Full link is %s' %link)
        # # Now we need to go to each URL for the actual video links. Turns out that some videos are in embed tags, others in iframe tags, some from youtube and some from blip.
        # try:
            # video = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            # if video.startswith('http://a.'):
                # video = 'http://blip.tv/play/%s.html' % (video[25:36])
        # except IndexError:
                # Log('Index error here.')
        # Log('video is %s' %video)
        # thumb = HTML.ElementFromURL(PLINKETT).xpath('./a/img')#[0].get('src')
        # #if len(thumb) is not 0:
        # #    Log('Thumbnail link %s' %thumb)
        # #else:
        # #    Log('No thumbnail found')
        # #    thumb = R(ICON)

        # oc.add(VideoClipObject(
                # url = video,
                # thumb = thumb))

        # if len(oc) >= MAX_EPISODES_PER_PAGE:
            # oc.add(NextPageObject(key = Callback(Plinkett, title = 'Mr. Plinkett', offset = counter), title = 'Next'))
            # return oc

    # return oc


###################################################################################################
@route('/video/redlettermedia/halfbag', offset = int)
def HalfBag(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
	
	# Pages are split up by year. Get list of videos from each page.
    for link in HITBMORE:
        link = HITB % (page)
        for video in HTML.ElementFromURL(link).xpath('//*[@class="post clearfix"]/div/p/a'):
               counter = counter + 1
               if counter <= offset:
	               continue			   
               url = video.xpath('//embed')
               thumb = video.xpath('./a/img')[0].get('src')
               Log('URL is %s' %url)
	
	oc.add(VideoClipObject(
		url = url,
		thumb = thumb))
		
	if len(oc) >= MAX_EPISODES_PER_PAGE:
        	oc.add(NextPageObject(key = Callback(AllShows, title = 'Half in the Bag', offset = counter), title = 'Next')) 
        	return oc

    return oc

###################################################################################################
@route('/video/redlettermedia/bestworst', offset = int)
def BestWorst(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
	
    for video in HTML.ElementFromURL(BOW).xpath('//*[@id="post-main-3857"]/div/p/a/@href'):
       	counter = counter + 1
        if counter <= offset:
	        continue		
	Log(video)
       	url = video
       	thumb = video #.xpath('./@src')[0]
       	Log('URL is %s' %url)
       	Log(thumb)

       	oc.add(VideoClipObject(
            url = url,
            thumb = thumb))
				
	if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(AllShows, title = 'Best of the Worst', offset = counter), title = 'Next')) 
            return oc

    return oc

###################################################################################################
@route('/video/redlettermedia/allshows', offset = int)
def AllShows(title, offset = 0):
    oc = ObjectContainer(title2 = title)
    
    counter = 0

    for video in XML.ElementFromURL(RSS_FEED).xpath('//item'):
        counter = counter + 1
        if counter <= offset:
	  continue
        Log('Video is %s' %video)
	url = video.xpath('./link')[0].text
        Log('URL is %s' %url)
	title = video.xpath('./title')[0].text
        date = video.xpath('./pubDate')[0].text
        date = Datetime.ParseDate(date)
        summary = video.xpath('./blip:puredescription', namespaces=NS)[0].text
        thumb = video.xpath('./media:thumbnail', namespaces=NS)[0].get('url')
        if thumb[0:4] != 'http': thumb = 'http://a.images.blip.tv' + thumb
        duration_text = video.xpath('./blip:runtime', namespaces=NS)[0].text
        duration = int(duration_text) * 1000

        oc.add(VideoClipObject(
              url = url,
              title = title,
              summary = summary,
              thumb = thumb,
              duration = duration,
              originally_available_at = date))
	
        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(AllShows, title = 'All Shows', offset = counter), title = 'Next'))
        #if len(oc) == 0:
	    #return ObjectContainer(header='No Results', message='No results were found')    
            return oc
    
    return oc
