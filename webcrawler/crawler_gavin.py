
#import requests as r
import csv
import time
import requests

# Global Settings.
global max_pages_to_crawl, max_runtime, site_timeout, url_length_limit

##Change these to limit search depth/time or change the seed(s)
#Max pages the program will visit
max_pages_to_crawl = 10
#Max time the program will run
max_runtime = 10
#Timeout in seconds that the program will wait for a response from a site
site_timeout = 5
#Max length of a URL (Avoid Spider Trap)
url_length_limit = 128
#Inital URL List. Can add/remove websites
seeds = ["https://informationsystems.umbc.edu/"]



#Main
#Initialize frontier, witch holds all the sites to crawl. Content should be stored as [URL, Visited Bool, Content]
global frontier
frontier = []

#Seed the frontier, add the inital seed links to the main frontier list
for seed in seeds:
    #Adds the Seed to Frontier. [URL, Visited Bool, Content]
    new_Site = [str(seed), 0, None]
    print("Seed: " + str(new_Site))
    frontier.append(new_Site)
    print(" Frontier: " + str(frontier))

#Crawler Class to store pinging the site, getting web content, and adding to the frontier
class Crawler:
    def getWebContent(url):
    #Returns HTML content of the site if pingable    
        start_time = time.time()
        
        print("Crawling: " + url)
        if (Crawler.ping(url) == 200):
            response = requests.get(url, timeout=site_timeout)
            print("Success fetching: " + response.url + " in " + str(round(time.time() - start_time, 2)) + " seconds")
            return response.content
        else:
            print("Failure fetching: " + url + " in " + str(round(time.time() - start_time, 2)) + " seconds")
            return
    def ping(url):
    #Checks if site is pingable/active before any attempt to crawl.
        try:
            #Returns status code (200=success) or -1 if unreachable
            print("Pinging: " + url)
            response = requests.get(url, timeout=site_timeout)
            return response.status_code
        except Exception as e:
            print("Failure pinging: " + url + ". Response Code: " + str(e))
            return -1
    def getURLs(htmlContent):
    #Returns an Array of URLS from html content & adds them to the frontier
        urlList = []
        #Makes sure to convert to string before any manipulation
        input = str(htmlContent)
        input = input.lower()
        #Runs through each character in the string
        link_count = 0
        for i in range(len(input)):
            #Check for beginning of a link tag

            #Check for beginning of a link (<a href= is beginning of a link in HTML) 
            if input[i:i+8] == "<a href=":
                link_count += 1
                for j in range(i, len(input)):
                    #Check for the end of the link, ">" for close of tag
                    end_of_link = input.find(">", j)
                    #print(input[i:end_of_link+1])
                    urlList.append(input[i:end_of_link+1])
                    #print(input[i:end_of_link+1])
                    break
        #After grabbing the links, go through and change to just the URL (remove tag)
        for url in urlList:
            final_url = url
            final_url = final_url.replace("<a href=", "")
            final_url = final_url.replace(">", "")
            final_url = final_url.replace("#", "")
            final_url = final_url.replace('"', "")
            final_url = final_url.replace(" ", "")
            #Check if URL is an HTTP link, sometimes other links are included (mail lists, etc)
            if final_url[0:4] == "http":
                #Check if URL is already in frontier, if not add.
                if final_url not in frontier:
                    frontier.append([final_url, 0, None])
                else:
                    print("URL already in frontier: " + final_url)

        print("Found " + str(link_count) + " links")
    def crawl():
        visited_sites_count = 0
        
        start_time = time.time()
        index = 0
        while (visited_sites_count <= max_pages_to_crawl) and index < len(frontier):
            #Check if current site has been visited
            print("Count Iterated: " + str(index) + " Visited Sites: " + str(visited_sites_count) + " Time: " + str(round(time.time() - start_time, 2)) + " seconds")
            current_site = frontier[index]
            if current_site[1] == 0:
                current_site[1] = 1
                #Get the content of the site
                current_site[2] = Crawler.getWebContent(current_site[0])
                #Add to frontier, if content is none (meaning the site was unreachable), then remove from frontier
                if current_site[2] is None:
                    print("Skipping to next site")
                    frontier.pop(index)
                    index += 1
                    continue
                Crawler.getURLs(current_site[2])
                visited_sites_count += 1
                index += 1
           



#Run!!!
Crawler.crawl()
#get count of frontier    
print("Frontier: " + str(len(frontier)))

#Store to txt
with open('results.txt', 'w') as f:
    for site in frontier:
        f.write(site[0] + '\n') 
        



        








