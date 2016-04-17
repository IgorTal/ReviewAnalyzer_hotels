import urllib2
import re
import json

# This program reads through Trip Advisor and collects user review data
# of hotels one city at a time.
# To use go to Trip Advisor and search for hotels from a city. For example:
# https://www.tripadvisor.com/Hotels-g58493-Gold_Bar_Washington-Hotels.html
# Copy the first half of the URL up to and including "g58493-" and store in url_city_front
# Copy the second half of the URL starting at and including "-Gold_Bar-" and store in url_city_rear
# Enter the path and filename of the output in the path variable

# The program will search through every review of every hotel in the chosen city
# ------ WARNING: This will take a long time in cities with many hotels which have many reviews. ------
# and output the reviews 1 at a time using the following format:
#
#Review1url:[reviewHotel, ReviewText, [score, maxScore], dateWritten, userName, numberOfReviewsWrittenByUser]



def getHighestHotelPage(html_text):
    # Get highest hotel page starting at first page of a city's hotels
    regex_pages = 'oa\d\d*0'
    page_strings = re.findall(regex_pages, html_text)
    highest_page = sorted([int(s[2:]) for s in page_strings])[-1]
    return highest_page


def getHighestReviewPage(review_url):
    # Get highest review page starting at first page of a hotel
    req = urllib2.Request(review_url, headers={'User-Agent': "Magic Browser"})
    html_text = urllib2.urlopen(req).read()

    regex_pages = '(?<=page-number=")\d*(?=")'
    page_strings = re.findall(regex_pages, html_text)
    highest_page = sorted([int(s) for s in page_strings])[-1]
    return highest_page


def getHotelsFromResultsPage(results_page_url):
    #return urls of individual hotels from search results page
    hotel_urls = []

    req = urllib2.Request(results_page_url, headers={'User-Agent': "Magic Browser"})
    html_text = urllib2.urlopen(req).read()

    #Avoid promotional hotel links near bottom of page, look_before_index1 works
    #for multiple pages, look_before_index2 works for single page of hotels
    look_before_index1 = html_text.find('Prices above are provided by partners for one room, double occupancy and do not include all taxes and fees. Please see our partners for full details')
    look_before_index2 = html_text.find('Still looking for a place to stay?')
    look_before_index3 = html_text.find('Stay in your own private vacation rental')
    if look_before_index2 == -1:
        look_before_index2 = '-1'
    html_text = html_text[:min(look_before_index1, look_before_index2, look_before_index3)]

    regex='\/Hotel_Review-g\d*-d\d*-Reviews.*?html'
    hotel_list = re.findall(regex, html_text)
    for hotel in hotel_list:
        hotel_urls.append('https://www.tripadvisor.com' + hotel)

    print 'searched for hotels in:', results_page_url
    print 'hotel links:', list(set(hotel_urls))
    return list(set(hotel_urls))


def getPageUrls(url_city_front, url_city_rear):
    #Get urls of pages with 30 hotels on each page. Return list of all hotel urls.
    hotel_urls_list=[]
    req = urllib2.Request(url_city_front + url_city_rear, headers={'User-Agent': "Magic Browser"})
    html_text = urllib2.urlopen(req).read()
    try:
        top_page = getHighestHotelPage(html_text)
    except:
        print 'Top hotel page not found, most likely only one page exists for this city'
        top_page = 0

    for page in range(0, top_page + 30, 30):
        print 'searching page', page/30+1, 'out of', top_page/30+1, 'for hotel urls in', url_city_rear[1:-12]
        results_page_url = url_city_front + str(page) + url_city_rear
        hotel_urls = getHotelsFromResultsPage(results_page_url)
        for hotel_url in hotel_urls:
            hotel_urls_list.append(hotel_url)
        break
    print 'found', len(list(set(hotel_urls_list))), 'hotels in', url_city_rear[1:-12]
    return list(set(hotel_urls_list))


def getReviewUrlsOnPage(hotel_url_front, hotel_url_rear, page):
    #Yields review urls as a list from given hotel url and page number

    hotel_url = hotel_url_front + 'or' + str(page) + '-' + hotel_url_rear
    print 'searching', hotel_url, 'for review links\n'

    req = urllib2.Request(hotel_url, headers={'User-Agent': "Magic Browser"})
    html_text = urllib2.urlopen(req).read()

    regex = '\/ShowUserReviews.*?.html'
    found_review_urls = re.findall(regex, html_text)
    review_urls_dups = ['https://www.tripadvisor.com' + end_url for end_url in found_review_urls]
    return list(set(review_urls_dups))


def getHotelName(html_text):
    # Returns name of the hotel
    try:
        regex = '(?<=Review of ).*(?= - TripAdvisor</title>)'
        return re.findall(regex, html_text)[0]
    except:
        return 'hotel name not found'


def getReviewText(html_text):
    #Gets body of review from html_text return text as string
    try:
        regex = '(?<=property="reviewBody" id="review_).*?(?=<\/p>)'
        text = re.findall(regex, html_text, re.DOTALL)[0]
        text = text[text.find('">\n') + 3:-1]

        return text.replace('<br/>', '\n')
    except:
        return 'text not found'


def getReviewRating(html_text):
    # Gets rating from html_text and returns as list where
    # 1st item is rating second item is max possible
    try:
        regex = '\d of \d'
        delete_after = '<span class="rate sprite-rating_s rating_s"> <img class="sprite-rating_s_fill rating_s_fill'
        delete_after_index = html_text.find(delete_after)
        html_text_snip = html_text[delete_after_index:delete_after_index+250]
        rating_string = re.findall(regex, html_text_snip)[0].split(' ')
        return [rating_string[0], rating_string[-1]]
    except:
        return 'rating not found'


def getReviewDate(html_text):
    #Returns date as a string in the format of 'July 30, 2015'
    regex = '(?<=property="datePublished">Reviewed ).*'
    try:
        return re.findall(regex, html_text)[0]
    except:
        return 'date not found'


def getReviewAuthor(html_text):
    # Returns author name as a string
    regex = '''(?<='show_reviewer_info_window', 'user_name_name_click'\)">).*(?=<)'''
    try:
        return re.findall(regex, html_text)[0]
    except:
        return 'author not found'


def getReviewCount(html_text):
    # Returns number of reviews written by author
    regex = '(?<=<span class="badgeText">).*(?= reviews)'
    try:
        return re.findall(regex, html_text)[0]
    except:
        return 'no reviews by author'


def getReviewInfo(review_url):
    #Calls functions to get review text, author name, star rating, number of reviews, date
    #from a review url and returns info in a dict where key is the review url and the value
    #is a list of data in various formats.

    req = urllib2.Request(review_url, headers={'User-Agent': "Magic Browser"})
    html_text = urllib2.urlopen(req).read()

    review_text = getReviewText(html_text)
    review_rating = getReviewRating(html_text)
    review_date = getReviewDate(html_text)
    review_author = getReviewAuthor(html_text)
    review_count = getReviewCount(html_text)
    review_hotel = getHotelName(html_text)

    yield {review_url: [review_hotel, review_text, review_rating, review_date, review_author, review_count]}


# def writeToFile(out_path, out_json):
#     out_file = open(out_path, 'w')
#     out_file.write(json.dumps(out_json))
#     out_file.close()


def main(url_city_front, url_city_rear):
    hotel_urls = getPageUrls(url_city_front, url_city_rear)

    city_name = url_city_rear[1:-12]
    out_dict = {city_name: {}}

    for hotel_url in hotel_urls:
        hotel_url_front = hotel_url[:hotel_url.find('Reviews-')+8]
        hotel_url_rear = hotel_url[hotel_url.find('Reviews-') + 8:]

        hotel_name = hotel_url_rear[:-4]
        out_dict[city_name][hotel_name] = {}

        #Get last page number of reviews to know when to stop looping through review pages
        try:
            highest_review_page = getHighestReviewPage(hotel_url_front + hotel_url_rear)
        except:
            print 'Top review page not found, most likely only one review exists for this hotel'
            highest_review_page = 0

        print 'hotel', hotel_url_rear[:15], 'has', highest_review_page, 'pages of reviews'
        for page in range(0, highest_review_page * 10, 10):
            review_urls = getReviewUrlsOnPage(hotel_url_front, hotel_url_rear, page)

            for review_url in review_urls:
                print json.dumps(getReviewInfo(review_url).next())

    # writeToFile(out_path, out_dict)

    print '\n\n------------Done With Search----------\n\n'


# out_path = 'C:\work\script\pythonScripts\HotelRatings\Arlington.txt'
url_city_front = 'https://www.tripadvisor.com/Hotels-g30272-' + 'oa'
url_city_rear = '-Arlington_Washington-Hotels.html'
main(url_city_front, url_city_rear)
