
from search import search
import re
import time as tm 
import sys
from instagrapi import Client
from time import sleep
import os
import random
from datetime import datetime



captions = [    
    "This little pup just stole my heart ❤️🐶 #doglovers #pawfect #trendingdogs #repost",    
    "If this video doesn't brighten up your day, I don't know what will 🌞🐾 #dogstagram #pawfect #trendingdogs #dogsofinstagram",    
    "I can't stop watching this video of the cutest pup ever 😍🐶 #pawfect #trendingdogs #dogsofinstagram #repost",    
    "This video makes me want to adopt a pup ASAP 🏠🐾 #dogrescue #pawfect #trendingdogs #dogsofinstagram"
]

dog_accounts = [
    'dogsofinstagram', 'goldenretrievers', 'puppystagrams', 'pugsofinstagram', 'doodlesofinstagram',
    'labradorsofinstagram', 'bulldogsofinstagram', 'corgisofinstagram', 'huskies', 'yorkiesofinstagram',
    'bordercolliesofinstagram', 'beaglesofinstagram', 'frenchiesofinstagram', 'gsdsofinstagram',
    'rottweilersofinstagram', 'chihuahuasofinstagram', 'dobermanpinscher', 'boxersofinstagram',
    'greyhounds', 'weimaranersofig', 'malteseofinstagram', 'sheltiesofinstagram', 'shihtzusofinstagram',
    'jackrussellsofig', 'englishcockerspaniel', 'whippets', 'dachshundsofinstagram', 'bostonterriers',
    'westiesofinstagram', 'schnauzersofinstagram', 'vizslasofinstagram', 'cockapoosofinstagram',
    'australianshepherdsofinstagram', 'greatdanesofinstagram', 'irish_setters_of_instagram',
    'lhasaapso', 'spaniels_of_instagram', 'poodlesofinstagram', 'pyreneesofinstagram',
    'houndsofinstagram', 'weinerdogworld', 'miniature_schnauzers', 'newfoundlandsofinstagram',
    'samoyedsofinstagram', 'affenpinscher', 'belgianshepherdsofinstagram', 'englishspringerspaniel',
    'frenchbulldogsofig', 'cavaliersofinstagram', 'shibainu_world', 'borderterriersofinstagram',
    'italiangreyhound', 'bullyinstafeature', 'malinoisworld', 'vizslalove', 'bullylifetv',
    'oldeenglishbulldogge', 'goldensofinsta', 'bulldogstuff', 'bulldogdays', 'bullyworldwide',
    'bulldoglovers', 'bulldogsonline', 'bullymagazine', 'boxerlovers', 'boxergram', 'boxerdogoftheday',
    'boxerworld', 'boxersofinstagram_', 'boxerworldfeature', 'labrador_', 'labradornation',
    'labradorable', 'labrador_lovers_club', 'labrador_feature', 'labradors_', 'labradorsofig',
    'labradorfanclub', 'labradoroftheday', 'labradormoments', 'blacklab_feature', 'chocolatelab_feature',
    'yellowlab_feature', 'labrador__retriever', 'labrador.lovers', 'blacklabradors_', 'corgifeature',
    'corgigram_', 'corgis_of_instworld', 'corgiplanet', 'corgis_of_insta', 'corgisarelove',
    'corgi.world.feature', 'corgilove.feature', 'corgisftw', 'corgiworldinspiration', 'pugloversclub',
    'pug_feature', 'pugloversworldwide', 'pugworld_', 'pugfanatics', 'pugsofigworld', 'pugseverywhere',
    'pugnation'
]

os.system('cls' if os.name == 'nt' else 'clear')

print("Hello Welcome to instaPYY!\nYou will now be asked if you need content scrapped, if you already have a csv folder with all the links to your videos!.\n   - If input is Y we will start the scraping procedure.\n   - If input is N you will be brought straight to the bot posting procedures.\n\n")

now = datetime.now()

def main():

    ##trying to delete all videos from downloade_videos folder, FOR SOME REASON CLIENT still uses the mp4 in the folder after posting the content

                                                    #clear_folder(r'C:\Users\clem3\OneDrive\Desktop\instaPYY\downloaded_videos')

    ## asking the user for the theme of his car page/ the search for content + asking if he already has the content

    dedicated_folder_answer = input('Do you need content scrapped from tiktok? (Y/N): ').upper()

    ## if answer is yes then we will only take the files in his folder and upload them in a certain interval, 
    # NO meaning that you already previously downloaded in a csv folder, we will then start to post this folder instead
    
    if dedicated_folder_answer == 'N':

        csv_folder_ = input('Enter the csv where links are stored: ')
        
        n_per_day  = int(input('Enter the number of videos you want to post per day: '))

        initialized_search = search("tiktok", None, None, csv_folder_, n_per_day, None, None)

        if input(f"your links stored in the 'InstaPYY_user_v/{initialized_search.csvfolder}.csv\nTo launch the bot initializing this number of post per days :'{initialized_search.number_of_vids_per_day}' run command 'GO' to stop the bot can go back to main menu input Crlt-C: ") == 'GO':
            
            username_ = input("Username of account: ")
            password_ = input("Password of account: ")

            cl = Client()
            cl.login(username=username_, password=password_)

            dog_accounts_number_ = 0

            while True:
                
                followed_users_ = []

                # catching ctrl-C to start another follow loop
                try:
                    
                    sleep(26220//n_per_day)

                    accounts_to_follow_id_ = cl.user_id_from_username(dog_accounts[dog_accounts_number_])
                    
                    dog_accounts_number_ +=1

                    followers_ = cl.user_followers(user_id=accounts_to_follow_id_, amount=15)

                    for user_ in followers_:
                        cl.user_follow(user_)
                        print(f"user: {cl.username_from_user_id(user_)} has been followed")
                        followed_users_.append(user_)
                        sleep(300)


                    dt_string_follow = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of follow =", dt_string_follow)
                    
                    print('starting download protocol')

                    sleep(28200//n_per_day)

                    # download procedures
                    mp4_file_ = initialized_search.download()

                    print(mp4_file_)

                    print('starting posting protocol')

                    max_retries = 3
                    retry_delay = 5

                    for i in range(max_retries):
                        try:
                            cl.clip_upload(f"downloaded_videos/{mp4_file_}", caption = f"{captions[random.randint(0, len(captions)-1)]}, , credits from tiktok: {mp4_file_[2:-7]}")
                            break
                        except Exception as e:
                            print(f"Error: {e}")
                            sleep(retry_delay)
                    
                    dt_string_post = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of post =", dt_string_post)

                    # unfollow procedure
                    
                    sleep(26220//n_per_day)

                    print("starting unfollow")

                    for user_id_ in followed_users_:
                        print(f"user: {cl.username_from_user_id(user_id_)} has been unfollowed")
                        sleep(300)
                        cl.user_unfollow(user_id_)

                    followed_users_.clear()
        
                    dt_string_unfollow = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of unfollow =", dt_string_unfollow)
                    
                except KeyboardInterrupt:
                    main()
                    os.system('cls')
        else:
            sys.exit('wrong launch command')


    ## if the answer is no then we will prompt him for some web scrapping

    elif dedicated_folder_answer == 'Y':

        user_topic_one, user_topic_two = input('Input a 2 word tiktok search for your topic: ').split(" ")

        ## asking for the amount of videos he will download and where the scrapped urls would go + checking if folder exists

        scrape_links = int(input("enter the number of pages long you want to scrape videos for: "))
        csv_folder = input("Enter the name of the CSV file to save the scraped URLs in: ")

        with open(f"{csv_folder}.csv", 'w') as creating_new_file:
            pass

        ##initializing the users search .links() will donwload links to a csv folder depending on the number of scrolls and the user topics

        number_of_vids = int(input("enter the number of vids per day: "))

        print("initializing search object...")

        initialized_search = search("tiktok", user_topic_one, user_topic_two, csv_folder, number_of_vids, None, scrape_links)

        print("scrapping for links... GET READY TO COMPLETE THE CAPTCHA.")

        sleep(5)

        initialized_search.links()

        print("links saved to folder!")

        sleep(5)

        ## initializing the posting for the bot itself

        os.system('cls' if os.name == 'nt' else 'clear')

        if input(f"your links of downloaded videos are now in the 'InstaPYY/{initialized_search.csvfolder}'\nTo launch the bot initializing this number of post per days '{initialized_search.number_of_vids_per_day}' run command 'GO' to stop the bot can go back to main menu input Crlt-C: ") == 'GO':

            print()
        
            username_ = input("username of account: ")
            password_ = input("password of account: ")

            cl = Client()
            cl.login(username=username_, password=password_)
            print("starting follow loop")

            dog_accounts_number = 0

            while True:

                followed_users = []

                # catching ctrl-C to start another follow loop
                try:

                    sleep(26220//number_of_vids)

                    accounts_to_follow_id = cl.user_id_from_username(dog_accounts[dog_accounts_number])

                    dog_accounts_number += 1
                    
                    # Retrieve up to 15 followers
                    
                    followers = cl.user_followers(user_id=accounts_to_follow_id, amount=15)
                        
                    
                    # Follow new users
                    for user in followers:
                        cl.user_follow(user)
                        print(f"user: {cl.username_from_user_id(user)} has been followed")
                        sleep(300)

                        followed_users.append(user)

                    
                    dt_string_follow = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of follow =", dt_string_follow)
                    
                    print('starting download protocol')

                    sleep(28200//number_of_vids)

                    # download procedures
                    mp4_file = initialized_search.download()

                    print(mp4_file)

                    print('starting posting protocol')

                    max_retries = 3
                    retry_delay = 5

                    for i in range(max_retries):
                        try:
                            cl.clip_upload(f"downloaded_videos/{mp4_file}", caption = f"{captions[random.randint(0, len(captions)-1)]}, , credits from tiktok: {mp4_file[2:-7]}")
                            break
                        except Exception as e:
                            print(f"Error: {e}")
                            sleep(retry_delay)
                    
                    dt_string_post = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of follow =", dt_string_post)
                    
                    
                    sleep(26220//number_of_vids)
                    
                    print("starting unfollow")
                    # Unfollow 
                    for user_id in followed_users:
                        print(f"user: {cl.username_from_user_id(user_id)} has been unfollowed")
                        cl.user_unfollow(user_id)
                        sleep(300)

                    followed_users.clear()

                    dt_string_unfollow = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("date and time of follow =", dt_string_unfollow)
                
                    
                except KeyboardInterrupt:
                    main()
                    os.system('cls')   
        else:
            sys.exit('wrong launch command.')    
    else:
        sys.exit('unkown input')

def clear_folder(path_to_folder):

    for filename in os.listdir(path_to_folder):
        file_path = os.path.join(path_to_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
 
if __name__ == '__main__':
    main()