
import hyperSel
import requests
import time
from bs4 import BeautifulSoup
def pirsa_thread():
    posts = []
    start = time.time()
    for i in range(1, 1250): #this number may change as they get more talks
        link = f"https://pirsa.org/talks?page=%2C{i}"
        # print("ITER:", i)
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        # views-field views-field-search-api-rendered-item
        link_tags = soup.find_all('div', class_="views-field views-field-search-api-rendered-item")
        for tag in link_tags:
            try:
                # colors.print_warning(tag)
                #print("============================================================")
                # Find the relevant <p> tag containing the speaker information
                speaker_tag = tag.find('p', class_='node speaker-profile speaker-name-institution')

                # Extract the speaker name
                speaker = speaker_tag.a.text
                #print("speaker    :", speaker)

                # Extract the speaker's institution
                institution = speaker_tag.span.text.strip()
                #print("institution:", institution)

                all_a_tags = tag.find_all("a")

                title = all_a_tags[1].text
                #print("title      :",title)

                try:
                    desc = tag .find("div", class_="field__item").text
                except: 
                    desc = ""
                desc = institution + " - " + desc 
                #print("desc       :", desc)

                url = all_a_tags[1]["href"]
                full_url = f"https://pirsa.org{url}"
                #print("full_url   :", full_url)
            
                #print("=============================================")
                posts.append([title, desc, full_url, "pirsa", speaker])
                
            except:
                continue

        # EVERY 50 ITER
        if i % 50 == 0:
            db.group_insert(posts)
            colors.logging_print_color(color="light_blue", text_to_color="pirsa", pre_text=F"DONE [{db.count_all_posts()}][NUM:{len(posts)}]", post_text=F"PIRSA - [{round(time.time() - start, 2)}]")
            posts = []
            time.sleep(60)
            start = time.time()
            

if __name__ == '__main__':
    print("hello world")
