import wikipedia
import nltk
import mwparserfromhell
import re

def get_first_sentence(entity):
    page = wikipedia.page(entity)
    text = page.content
    first_sent = str(nltk.sent_tokenize(text)[0])

    return first_sent

# strip all the refs and templates in wikitext
# return cleaned wikitext and the entity name
def parse_text(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    first_section =str(wikicode.get_sections()[0])
    
    # find the entity name of this wikitext
    first_start_set = 0
    start = 0
    end = 0
    for i in range(len(first_section)):
        if first_section[i] == "\'" and first_section[i+1] == "\'" and first_section[i+2] == "\'":
            if first_start_set == 0:
                first_start_set = 1
                start = i+3
            else:
                end = i
    # get the first sentence of the wikipedia summery for this entity
    entity = first_section[start:end]
    first_sent = get_first_sentence(entity)
    
    # strip all refs and templates in wikitext
    main_text = first_section[start-3:]
    main_text = re.sub('<.*?>', '', main_text)
    main_text = re.sub('{{.*?}}', '', main_text)
   
    #get the summary(first sentence) of the main text
    last_word = nltk.word_tokenize(first_sent)[-2] #[-1] would be "."
    length = len(last_word)
    summary_end = 0

    for i in range(len(main_text)):
        if main_text[i] == last_word[0]:
            if main_text[i:i+length] == last_word:
                print "yooo"
                if main_text[i+length] == '.': # last word ending with '.' 
                    summary_end = i+length+1
                    break
                # last word ending with ']].'
                elif main_text[i+length] == ']' and main_text[i+length+1] == ']' and main_text[i+length+2] == '.':
                    summary_end = i+length+3
                    break
    print main_text
    print last_word
    print summary_end
    return main_text[:summary_end]

if __name__ == "__main__":
    with open('sample1.txt', 'r') as f:
        wikitext = f.read()
    print parse_text(wikitext)
