# Get urls to txts
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request

import time
from threading import Thread
import os

class GetImagesfromPages():
    def __init__(self, nThreads, npage, url_page):
        self.nThreads = nThreads
        self.npage = npage
        self.url_page = url_page

        self.result_urls = []
    
    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def get_all_images(self, url):
        """
        Returns all image URLs on a single `url`
        """
        soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
        urls = []
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")

            if not img_url:
                # if img does not contain src attribute, just skip
                continue

            # make the URL absolute by joining domain with the URL that is just extracted
            img_url = urljoin(url, img_url)
            # remove URLs like '/hsts-pixel.gif?c=3.2.5'
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            # finally, if the url is valid
            if self.is_valid(img_url):
                urls.append(img_url)

        return urls
    
    # Func target
    def main(self, start, end):
        
        for i in range(start,end):
            try:
                self.result_urls.extend(self.get_all_images(self.url_page + str(i)))
            except:
                pass
        
    def __call__(self):
        
        # Create Threads
        threads = []
        
        batch = self.npage//self.nThreads
        for i in range(0, self.npage, batch):
            start = i
            end = i + batch
           
            if end >= self.npage:
                end = self.npage + 1

            threads.append(Thread(target=self.main, args = (start, end)))
        
        start = time.time()
        for i in range(self.nThreads):
            threads[i].start()
        for i in range(self.nThreads):
            threads[i].join()
        end = time.time()
        
        print(f"Time handle pages = {end - start:.2f}s", )
    
        return self.result_urls

def urls_to_txts(topic_names, topics, urltopic, n_page, n_threads):
    for dir, names in zip(topic_names, topics):
        dir_path_urls = f"./data/{dir}/urls"
        if not os.path.exists(dir_path_urls):
            os.makedirs(dir_path_urls)

        for name in names:
            result_of_name = []
            for key in urltopic.keys():
                res = GetImagesfromPages(min(n_threads, n_page//2), n_page, 
                                urltopic[key].format(name = name))()
                
                if len(res) > 0:
                    res = list(set(res))
                    result_of_name.extend(res)

            print(f"{dir_path_urls}/{dir}_{name}.txt have {len(result_of_name)} images \n")
            strResult = '\n'.join(result_of_name)
            with open(f"{dir_path_urls}/{dir}_{name}.txt", "w") as f:
                f.write(strResult)

if __name__ == '__main__':

    animal  =  ["Monkey",  "Elephant",  "cows",  
    "Cat",  "Dog",  "bear",  "fox",  "Civet", 
    "Pangolins", "Rabbit", "Bats", "Whale", 
    "Cock", "Owl", "flamingo", "Lizard", "Turtle", 
    "Snake", "Frog", "Fish", "shrimp", "Crab", "Snail", 
    "Coral", "Jellyfish", "Butterfly", "Flies", "Mosquito", 
    "Ants", "Cockroaches", "Spider", "scorpion", "tiger", 
    "bird",  "horse", "pig", "Alligator" ,"Alpaca" , 
    "Anteater", "donkey", "Bee", "Buffalo", "Camel", 
    "Caterpillar", "Cheetah", "Chicken",  "Dragonfly", 
    "Duck", "panda", "Giraffe"]

    plant = ["Bamboo", "Apple", "Apricot", "Banana", "Bean", 
    "Wildflower", "Flower", "Mushroom", "Weed", "Fern" , "Reed", 
    "Shrub", "Moss", "Grass", "Palmtree", "Corn", "Tulip", "Rose",
    "Clove", "Dogwood", "Durian", "Ferns", "Fig", "Flax", "Frangipani", 
    "Lantana", "Hibiscus", "Bougainvillea", "Pea", "OrchidTree", "RangoonCreeper",
    "Jackfruit", "Cottonplant", "Corneliantree", "Coffeeplant", "Coconut"
    , "wheat", "watermelon", "radish", "carrot"]

    furniture = ["bed", "cabinet", "chair", "chests", "clock", 
    "desks", "table", "Piano", "Bookcase", "Umbrella", "Clothes", 
    "cart", "sofa", "ball", "spoon", "Bowl", "fridge", "pan", "book"]

    scenery = ["Cliff", "Bay", "Coast", "Mountains", "Forests", 
    "Waterbodies", "Lake", "desert", "farmland", "river", "hedges", 
    "plain", "sky", "cave", "cloud", "flowergarden", "glacier", 
    "grassland", "horizon", "lighthouse", "plateau", "savannah", "valley", "volcano", "waterfall"]

    urltopic = {
        "freeimages": "https://www.freeimages.com/search/{name}/"
    }

    topic_names = ["animal", "plant", "furniture", "scenery"]
    topics = [animal, plant, furniture, scenery]
    n_threads = 3
    n_page = 6

    urls_to_txts(topic_names=topic_names, topics=topics, urltopic=urltopic, n_page=n_page, n_threads=n_threads)

