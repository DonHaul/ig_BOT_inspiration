#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!pip install instauto
#!pip install pillow


# In[4]:


from instauto.api.client import ApiClient
from instauto.api.actions import post as ps
import json
import requests

from PIL import Image
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os


# In[11]:


#fetch credentials
creds={}


if(os.path.isfile('credentials.json') ):
    with open('credentials.json',encoding='utf-8') as json_file:
        creds = json.load(json_file)
else:
    creds['username'] = os.getenv('username')
    creds['password'] = os.getenv('password')

    

print(creds)


# In[424]:


#grab quote from the web quote api



#GET "https://quotes.rest/qod?language=en" -H "accept: application/xml"

response = requests.get(
    'https://quotes.rest/qod?language=en',
    #params={'q': 'requests+language:python'},
    headers={'Accept': 'application/json'},
)

data = response.json()
quote= data['contents']['quotes'][0]


# In[446]:


W, H = (1080,1080)
    
img = Image.new('RGB', (W, H), color = 'black')

draw = ImageDraw.Draw(img)


font = ImageFont.truetype("./Fonts/Roboto-MediumItalic.ttf", 80)

#text splitting function, adds space for  long strings
text = quote['quote']



# In[447]:


import math



def AddNewLines(text,font,imgW=1080):

    outputtext=text
    w, h = draw.textsize(outputtext, font=font)
    numberoflines = math.ceil(w/imgW)
    print(numberoflines)

    for i in range(1,numberoflines):
        print("Space", i)

        startat= int(len(outputtext)*(i/numberoflines))
        print(startat)

        if(text[startat]!=' '):    
            for j in range(1,20):

                if text[startat+j]==' ':
                    startat=startat+j
                    print("BREAK1")
                    break
                elif text[startat-j]==' ':
                    startat=startat-j
                    print("BREAK2")
                    break
        print(text[startat])

        outputtext = outputtext[0:startat]+"\n"+outputtext[startat+1:len(outputtext)]

    w, h = draw.textsize(outputtext, font=font)


    print(w,h)

    return outputtext



text=AddNewLines(text,font,imgW=1080)

w, h = draw.textsize(text, font=font)

draw.text(((W - w) / 2, (H - h) / 2),text,(255,255,255),font=font,align="center")


#add author text
font = ImageFont.truetype("./Fonts/Roboto-Medium.ttf", 60)
authortext ="~"+quote['author']
w, h = draw.textsize(authortext, font=font)


# In[448]:



draw.text((W-100-w, H-h-100),authortext,(255,255,255),font=font)
im1 = img.resize((480,480)) 
# Shows the image in image viewer 

import datetime


#img.save("post_")


#generate story
W, H = (1080,1920)
    
imgStory = Image.new('RGB', (W, H), color = 'black')

drawStory = ImageDraw.Draw(img)


offset = (0, (1920 - 1080) // 2)
imgStory.paste(img, offset)


name = "./Posts/post.jpg"# + datetime.datetime.now().strftime('%y-%m-%d %H_%M_%S')+".jpg"
storyname = "./Posts/story.jpg"

img.save(name)
imgStory.save(storyname)


# In[ ]:


tagstring=""

#fetch tags
for t in quote['tags']:
    tagstring=tagstring+"#"+t+" "
    
caption = quote['quote']+"\n~"+quote['author'] + "\n\n"+tagstring


# In[13]:





if os.path.isfile('./instauto.save'):
    client = ApiClient.initiate_from_file('./instauto.save')
else:
    client = ApiClient(user_name=creds["username"], password= creds["password"])
    client.login()
    client.save_to_disk('./instauto.save')

    # get user info by username
    #i_uname = Info(username="")
    #info_username = client.profile_info(i_uname)
    #print(info_username)

    # get user info by user id
    #i_id = Info(user_id="")
    #info_id = client.profile_info(i_id)
    #print(info_id)


# In[12]:


creds


# In[454]:



post = ps.PostFeed(
    path=name,
    caption=caption
)
resp = client.post_post(post, 80)
print("Success: ", resp.ok)

post = ps.PostStory(
    path=storyname,
)
resp = client.post_post(post, 80)
print("Success: ", resp.ok)


# In[399]:





# In[405]:





# In[451]:


data

