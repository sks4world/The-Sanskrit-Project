#!/usr/bin/env python
# coding: utf-8

# || ॐ श्री महा पेरियवा सरणं ||
# 
# Ramayana, Aranya Kanda, references search for specific interests
# 
# || ॐ शान्ति शान्ति शान्तिः ||

# In[1]:


# Import data frame and visualization libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')

# Import Requests libraries (alternative for Selenium in some cases) for webscraping
import requests

# Import library to convert to html table
import df2img


# In[2]:


# Set path variables

prjPth = 'D:\\pth\\pth\\pth\\pth'
dtaPth = os.path.join(prjPth, '1_Data')
inpDtaPth = os.path.join(dtaPth, 'inp')
opDtaPth = os.path.join(dtaPth, 'op')
opFigPth = os.path.join(opDtaPth, 'figs')


# In[3]:


# Construct URLs
def construct_url_frm_pattern(chptrNum):
    bURL = 'url' # Contact me for this
    sarga = 'sarga'+ str(i+1)
    pg = '/aranyasans' + str(i+1) + '.htm'
    url = bURL + sarga + pg
    return(url)


# In[4]:


# Webscraping
def scrpe_frm_url_alt_utf8(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
    else:
        soup = ''
    return(soup)


# In[5]:


# Search for patterns in the html
def find_patterns_in_html(htmlText):
    lnsWithPtrnQ = []
    lnsWithPtrn = []
    soup = htmlText
    # Pattern to search for
    # Listing some known patterns in each page to make sure it works (quality check)
    # And then adding the required patterns
    ptrnQual = ["प्रविश्य", "भूतानाम्", "आकारम्"]              # For quality checks (some known values, to see if the code works)
    ptrnMeat = ["आमिस्", "पिशित", "मांस", "मांसं", "मांसम्"]   # Actual patterns interested in
    
    
    # Find lines containing the pattern
    for ptrn in ptrnQual:
        lnsWithPattern = [line.strip() for line in soup.get_text().split('\n') if ptrn in line]
    
        # Append the lines containing the pattern to the list (Quality)
        for line in lnsWithPattern:
            lnsWithPtrnQ.append(line)
    for ptrn in ptrnMeat:
        lnsWithPattern = [line.strip() for line in soup.get_text().split('\n') if ptrn in line]

        # Append the lines containing the pattern to the list (Actual interest)
        for line in lnsWithPattern:
            lnsWithPtrn.append(line)
    return(lnsWithPtrnQ, lnsWithPtrn)


# In[6]:


# Display dataframe as html table

def create_html_table_from_dta_frm(inp_dta_frm, op_path_fn, fig_size, inp_col_width, title_txt):
    
    fig = df2img.plot_dataframe(
    inp_dta_frm,
    col_width = inp_col_width,
    title=dict(
        font_color="black",
        font_family="Times New Roman",
        font_size=16,
        text = title_txt,
    ),
    tbl_header=dict(
        align="right",
        fill_color="gray",
        font_color="white",
        font_size=10,
        line_color="darkslategray",
    ),
    tbl_cells=dict(
        align="right",
        line_color="darkslategray",
    ),
    row_fill_color=("#ffffff", "#d7d8d6"),
    #fig_size=(400, 500),
    fig_size = fig_size,
    )

    df2img.save_dataframe(fig=fig, filename=op_path_fn)


# In[ ]:


# Main program
lnsWithPtrnQ = []
lnsWithPtrn = []
chptrNum = list(range(0,75))
lpCnt = 0
for i in chptrNum:
    lpCnt += 1
    url = construct_url_frm_pattern(i)
    htmlText = scrpe_frm_url_alt_utf8(url)
    lnsWithPtrnQ, lnsWithPtrn = find_patterns_in_html(htmlText)
    dtaDctQ = {'Lines with pattern': lnsWithPtrnQ}
    dtaDct = {'Lines with pattern': lnsWithPtrn}
    
    # Write to dataframe
    # Quality check
    tmpDtaFrmQ = pd.DataFrame.from_dict(dtaDctQ)
    tmpDtaFrmQ['URL'] = url
    tmpDtaFrmQ['Chapter'] = str(i+1)
    # Real data (of interest)
    tmpDtaFrm = pd.DataFrame.from_dict(dtaDct)
    tmpDtaFrm['URL'] = url
    tmpDtaFrm['Chapter'] = str(i+1)
    
    if lpCnt == 1:
        lnsWthPtrnQ = tmpDtaFrmQ
        lnsWthPtrn = tmpDtaFrm
    else:
        lnsWthPtrnQ = pd.concat([lnsWthPtrnQ, tmpDtaFrmQ])
        lnsWthPtrn = pd.concat([lnsWthPtrn, tmpDtaFrm])
    
        # control number of chapters read
        if lpCnt >= 77:
            break


# In[ ]:


# Display as html table and save table to output image
dtaFrmDis = lnsWthPtrnQ

Num = list(range(len(dtaFrmDis)+1))
del Num[0]
dtaFrmDis['Num'] = Num
dtaFrmDis = dtaFrmDis[['Num', 'URL', 'Chapter', 'Lines with pattern']]
dtaFrmDis = dtaFrmDis.set_index('Num')

figOutFn = os.path.join(opFigPth, 'tbl1.png')
figSz = (790,dtaFrmDis.shape[0]*60)
colWdth = [0.24, 3, 0.36, 1.6]
ttlTxt = 'Lines with patterns searched (Quality)'
create_html_table_from_dta_frm(dtaFrmDis, figOutFn, figSz, colWdth, ttlTxt)


# In[ ]:


# Manual verifications, annotations, explanations

trDta = ['1. The illustrious Rama saw the circle of ascetic hermitages', 
        '2. I am a demon named Viragha in this forest and this fortress, O sage I roam about armed with weapons daily eating meat',
        '3. The fire burnt down that great soul Sharabhanga from head-hair to body hair and thus his shrunk skin, bones and whatever flesh and blood are there, they are also burnt completely.',
        '4. Same as above',
        '5. They are attacked by demons who are very invincible and eat meat',
        '6. The sages dwelling in Dandaka forest are being eaten away by fiendish demons that subsist on human flesh',
        '7. See long translation text I below, story in context needed to understand',
        '8. Worshipping the fire, giving water and worshipping the guest a hermit should receive a guest and feed him, and if a hermit practices contrarily, oh, Rama, he is destined to eat his own flesh like a false deponent in other world say, hell',
         '9. See long translation text I below, story in context needed to understand',
         '10. Same as above',
         '11. Khara spoke this sentence "What for your are howling again when I have just now commanded those fearless flesh eating demons in order to fulfill your wish"',
        '12. Besides, those flesh-eating demons that have followed me are also felled by Rama',
         '13. Cacophonous and carnivorous predators and vultures took over the nearby places of Janasthaana and they made raucous sounds of many kinds',
         '14. That (Khara \'s) army of raw-flesh eaters with their bows, embellishments, and chariots',
         '15. That forest which became sludgy with the flesh and blood of killed demons',
         '16. highly fiery demon and devourer of raw-flesh Trishira',
         '17. I rambled Dandaka forest causing terror to the world, and eating the fleshes of sages." Thus Maareecha started to narrate his experience with Rama.',
         '18. (Mareecha says) On becoming a gigantic carnivorous animal I was on the rove in Dandaka forest while getting at Rama',
         '19. (Mareecha says) drinking off their (saints in Dhandaka forest) blood and feasting on their flesh',
         '20. Kings pursuing games of hunting in great forests, oh, Lakshmana, will be felling deer either for the sake of flesh, or just for the purpose of sporting archery',
         '21. Raghava then on killing another spotted deer and on taking its flesh, he hurried himself towards Janasthaana',
         '22. Same as above',
         '23. he (Ravana) gave audience to eight highly vigorous demons, the feasters on raw-flesh',
         '24. (Ravana said) Oh, gnarled demonesses of grisly mien and devourers of meat and blood, you have to indeed remove her (Sita mata\'s) pride immediately',
         '25. Raw-flesh eating demons are distraught as I have liquidated Khara',
         '26. (Rama laments) the raw-flesh gorgers must have gorged that youngish lady (Sita mata)',
         '27. On drawing up the flesh of that Rohi animal and lumping it to gobbets, that highly observant (of religious ceremonies) Rama placed those gobbets on pleasant greenish pasturelands as obsequial offerings in respect of that bird Jataayu',
         '28. With his expertise that straightforward monkey Sugreeva is indeed conversant with all of the strongholds of anthropophagite (human flesh eater) demons '
        ]

lnsWthPtrn['Translation'] = trDta
#lnsWthPtrn['Translation'] = 'To be filled'


# In[ ]:


# Display as html and save to image
dtaFrmDis = lnsWthPtrn

Num = list(range(len(dtaFrmDis)+1))
del Num[0]
dtaFrmDis['Num'] = Num
dtaFrmDis = dtaFrmDis[['Num', 'URL', 'Chapter', 'Lines with pattern', 'Translation']]
dtaFrmDis = dtaFrmDis.set_index('Num')

figOutFn = os.path.join(opFigPth, 'tbl2.png')
figSz = (900,dtaFrmDis.shape[0]*100)
colWdth = [0.24, 3, 0.36, 1.6, 2.5]
ttlTxt = 'Lines with patterns searched (words that mean Meat in Sanskrit)'
create_html_table_from_dta_frm(dtaFrmDis, figOutFn, figSz, colWdth, ttlTxt)


# In[ ]:


# Manual checks, annotations, translation verification and context of an entire sarga where needed


sloka = ['इह एकदा किल क्रूरो वातापिः अपि च इल्वलः \| भ्रातरौ सहितौ आस्ताम् ब्राह्मणघ्नौ महा असुरौ \|\| ४-११-५५',
        'धारयन् ब्राह्मणम् रूपम् इल्वलः संस्कृतम् वदन् \| आमंत्रयति विप्रान् स श्राद्धम् उद्दिश्य निर्घृणः \|\| ४-११-५६',
         'भ्रातरम् संस्कृतम् कृत्वा ततः तम् मेष रूपिणम् \| तान् द्विजान् भोजयामास श्राद्ध दृष्टेन कर्मणा \|\| ४-११-५७',
         'ततो भुक्तवताम् तेषाम् विप्राणाम् इल्वलो अब्रवीत् \| वातापे निष्क्रमस्व इति स्वरेण महता वदन् \|\| ४-११-५८',
         'ततो भ्रातुर् वचः श्रुत्वा वातापिः मेषवत् नदन् \| भित्त्वा भित्वा शरीराणि ब्राह्मणानाम् विनिष्पतत् \|\| ४-११-५९',
         'ब्राह्मणानाम् सहस्राणि तैः एवम् काम रूपिभिः \| विनाशितानि संहत्य नित्यशः पिशित अशनैः \|\| ४-११-६०',
        'अगस्त्येन तदा देवैः प्रार्थितेन महर्षिणा \| अनुभूय किल श्राद्धे भक्षितः स महा असुरः \|\| ४-११-६१',
         'ततः संपन्नम् इति उक्त्वा दत्त्वा हस्ते अवनेजनम् \| भ्रातरम् निष्क्रमस्व इति च इल्वलः समभाषत \|\| ४-११-६२',
         'स तदा भाषमाणम् तु भ्रातरम् विप्र घातिनम् \| अब्रवीत् प्रहसन् धीमान् अगस्त्यो मुनि सत्तमः \|\| ४-११-६३',
         'कुतो निष्क्रमितुम् शक्तिर् मया जीर्णस्य रक्षसः \| भ्रातुः ते मेष रूपस्य गतस्य यम सादनम् \|\| ४-११-६४'
        ]


translation = ['Once upon a time verily cruel demon brothers Vaataapi and Ilvala were here together, \
           and they the dreadful demons, they say, used to be Bhraman-killers. 4-11-55',
               'Disguising in Bhraman\'s semblance and speaking sophisticatedly that Ilvala used to invite Brahmans\
              for the purpose of obsequial ceremonies, where Brahman are fed after usual ceremony to \
              appeases their manes. 4-11-56',
              'Then Ilvala used to make his brother Vaataapi into a ram, perfect that ram\'s meat into deliciously \
         cooked food, and used to feed Brahmans according to obsequial rites and deeds. 4-11-57',
               'When those Brahmans are surfeited with that ram\'s meat, then Ilvala used to shout loudly, \
               "oh, Vaataapi, you may come out." 4-11-58',
               'Then on listening his brother\'s words Vaataapi used to lunge out bleating like a ram, \
               tearing and rending the bodies of those Brahmans. 4-11-59',
               'This way they the guise changing demons always ruined thousands of Brahmans together, \
               greedy for raw-flesh as they are. 4-11-60',
               'Then by Sage Agastya, whom gods have prayed to end this demonic menace, and whom demon Ilvala \
               invited to feast during obsequial rites, he that Agastya having relished the fiendish demon in the form of ram, \
               they say, had finished him off. 4-11-61',
               'Then Ilvala while giving lateral hand wash into the palms of Agastya entered in the routine conversation \
               of obsequies asking, "Is this rite fulfilled..." and he furthered it in calling his brother to come out. 4-11-62',
               'Then that wise and eminent sage Agastya spoke mockingly to Ilvala who is \
               conversing that way to his brother to come out. 4-11-63',
               'Where is the energy for that ram shaped demon brother of yours to come out as \
               I digested and sent him to the hellish residence of Terminator. [4-11-64]'
              ]

cntxtDta = {'Sloka': sloka,
           'Translation': translation,
           }


# In[ ]:


# Display as html table and save table as image
cntxtDtaFrm = pd.DataFrame.from_dict(cntxtDta)
cntxtDtaFrm['Chapter'] = '11'
cntxtDtaFrm['Kanda'] = 'Aranya Kanda'

dtaFrmDis = cntxtDtaFrm

Num = list(range(len(dtaFrmDis)+1))
del Num[0]
dtaFrmDis['Num'] = Num
dtaFrmDis = dtaFrmDis[['Num', 'Chapter', 'Kanda', 'Sloka', 'Translation']]
dtaFrmDis = dtaFrmDis.set_index('Num')

figOutFn = os.path.join(opFigPth, 'tbl3.png')
figSz = (900,dtaFrmDis.shape[0]*100)
colWdth = [0.24, 0.3, 0.4, 2, 3]
ttlTxt = 'Long translation text, story in context needed to understand'
create_html_table_from_dta_frm(dtaFrmDis, figOutFn, figSz, colWdth, ttlTxt)


# In[ ]:


# Manual checks, annotations, translation verification and context of an entire sarga where needed

sloka = ['Introduction',
         'ताम् तथा पतिताम् दृष्ट्वा विरूपाम् शोणित उक्षिताम् \| भगिनीम् क्रोध संतप्तः खरः पप्रच्छ्ह राक्षसः \|\| ३-१९-१',
         'उत्तिष्ठ तावत् आख्याहि प्रमोहम् जहि संभ्रमम् \| व्यक्तम् आख्याहि केन त्वम् एवम् रूपा विरूपिता \|\| ३-१९-२',
         'न हि पश्यामि अहम् लोके यः कुर्यात् मम विप्रियम् \| अमरेषु सहस्राक्षम् महएन्द्रम् पाकशासनम् \|\| ३-१९-७',
         'अद्य अहम् मार्गणैः प्राणान् आदास्ये जीवितांतगैः \| सलिले क्षीरम् आसक्तम् निष्पिबन् इव सारसः || ३-१९-८',
         'निहतस्य मया संख्ये शर संकृत्त मर्मणः \| सफेनम् रुधिरम् कस्य मेदिनी पातुम् इच्छ्हसि \|\| ३-१९-९',
         'कस्य पत्ररथाः कायात् मांसम् उत्कृत्य संगताः \| प्रहृष्टा भक्षयिष्यन्ति निहतस्य मया रणे || ३-१९-१०'
         
        ]
translation = ['Shuurpanakha narrates her woeful story to her brother Khara ncriminating Seetha in particular. She wants Khara to wage a war so that she could drink Seetha\'s blood. \
Khara in order to appease his sister sends fourteen demons to eliminate Rama.',
               'On seeing her who fell before him in a misshapen and blood-soaked condition, demon Khara is all stewed up and asked her. 3-19-1',
               'Rise up, first tell me clearly putting away your flurry and fluster, who disfigured your form in this way. 3-19-2',
               'Indeed, I do not find anyone who causes displeasure to me in this world, even among divinities including the thousand eyed Indra, the controller of demon Paaka. 3-19-7',
               'Now, I will take away the lives of that miscreant with my arrows that are terminators of lives, as a swan would drink milk to dregs even if it is mingled in water, duly separating milk from water. 3-19-8',
               'Whose frothy blood is it that the earth wishes to quaff when I cut off his crucial organs by my arrows and drop him dead in a combat. 3-19-9',
               'Whose body is it from which birds pressing round gladly wish to wring flesh to pieces for eating when I slay him in war. 3-19-10'
              ]

cntxtDta1 = {'Sloka': sloka,
           'Translation': translation,
           }


# In[ ]:


cntxtDtaFrm = pd.DataFrame.from_dict(cntxtDta1)
cntxtDtaFrm['Chapter'] = '11'
cntxtDtaFrm['Kanda'] = 'Aranya Kanda'

dtaFrmDis = cntxtDtaFrm

Num = list(range(len(dtaFrmDis)+1))
del Num[0]
dtaFrmDis['Num'] = Num
dtaFrmDis = dtaFrmDis[['Num', 'Chapter', 'Kanda', 'Sloka', 'Translation']]
dtaFrmDis = dtaFrmDis.set_index('Num')

figOutFn = os.path.join(opFigPth, 'tb4.png')
figSz = (900,dtaFrmDis.shape[0]*100)
colWdth = [0.24, 0.3, 0.4, 2, 3]
ttlTxt = 'Long translation text, story in context needed to understand'
create_html_table_from_dta_frm(dtaFrmDis, figOutFn, figSz, colWdth, ttlTxt)

