import wikipedia
import nltk
import mwparserfromhell
import re

def get_links(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    section = wikicode.get_sections()[0]

    #get links for first section
    links = section.filter_wikilinks()
    entities = []
    
    for link in links:
        if link.text != None:
            text = link.text.encode('utf-8').strip()
        else:
            text = link.title.encode('utf-8').strip()
        entities.append(text)

    print entities
    return entities
    

def get_first_sentence(title):
    try:
        page = wikipedia.summary(title)
    except wikipedia.exceptions.DisambiguationError as e:
        return None
    except AttributeError as e:
        return None
    
    text = page
    sents = nltk.sent_tokenize(text)
    if len(sents) <= 0:
        return None
    
    first_sent = (nltk.sent_tokenize(text)[0]).encode('utf-8').strip()

    return first_sent

# strip all the refs and templates in wikitext
# return the first sentence of wikitext
def parse_text(page):
    wikitext = page
    wikicode = mwparserfromhell.parse(wikitext)

    sections = wikicode.get_sections()
    if len(sections) <= 0:
        return
    first_section = (wikicode.get_sections()[0]).encode('utf-8').strip()

    # get the first sentence of the wikipedia summery for this entity
    # page_id = id_and_page[0]
    # #print page_id
    # first_sent = get_first_sentence(page_id)
    # if first_sent == "":
    #     # disamguition page, ignore it
    #     return

    #strip {{Infobox ...}}
    main_text = re.sub(r'\n', '', first_section)
    #print main_text
    box_tag = "{{Infobox"
    box_tag_end = "}}'''"
    box_start = 0
    box_end = 0
    for i in range(len(main_text)):
        if main_text[i] == "{" and main_text[i:i+len(box_tag)] == box_tag:
            #print main_text[i:i+len(box_tag)]
            box_start = i
        if main_text[i] == "}" and main_text[i+1] == "}" and main_text[i+2] == "\'" and main_text[i+3] == "\'" and main_text[i+4] == "\'":
            print "~~~~~~~~~~~~~~~~~~~~~~~~~"
            print main_text[i:i+5]
            box_end = i+2
            break
    main_text = main_text[box_end:]
    print main_text
    #print main_text
    main_text = re.sub(r'\{[^)]*\}', '', main_text)
    main_text = re.sub(r'\<[^)]*\>', '', main_text)
    #print main_text
    #find the start of main text by locating '''
    start = 0
    for i in range(len(main_text)):
        if main_text[i] == "\'" and main_text[i+1] == "\'" and main_text[i+2] == "\'":
            start = i
            break
    main_text = main_text[start:]
    # strip all refs and templates in wikitext
    #main_text = re.sub(r'\{[^)]*\}', '', main_text)
    #main_text = re.sub(r'\<[^)]*\>', '', main_text)

    #get the summary(first sentence) of the main text
    # last_word = nltk.word_tokenize(first_sent)[-2] #[-1] would be "."
    # length = len(last_word)
    # summary_end = 0
    #
    # for i in range(len(main_text)):
    #     if main_text[i] == last_word[0]:
    #         if main_text[i:i+length] == last_word:
    #             if main_text[i+length] == '.': # last word ending with '.'
    #                 summary_end = i+length+1
    #                 break
    #             # last word ending with ']].'
    #             elif main_text[i+length] == ']' and main_text[i+length+1] == ']' and main_text[i+length+2] == '.':
    #                 summary_end = i+length+3
    #                 break
    #print main_text
    #print last_word
    #print summary_end
    #return main_text[:summary_end]

if __name__ == "__main__":
    with open('sample1.txt', 'r') as f:
        wikitext = f.read()
    get_links(wikitext)
