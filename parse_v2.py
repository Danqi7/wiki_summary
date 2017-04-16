import wikipedia
import nltk
import mwparserfromhell

def get_links(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    section = wikicode.get_sections()[0]

    #get links for first section
    links = section.filter_wikilinks()
    entities = []

    for link in links:
        if link.text != None:
            text = link.text
        else:
            text = link.title
        text = text.encode('utf-8').strip()
        entities.append(text)

    return set(entities)


def get_first_sentence(title):
    try:
        page = wikipedia.summary(title)
    #except wikipedia.exceptions.DisambiguationError as e:
    except Exception as e:
        return None
    except AttributeError as e:
        return None

    text = page
    sents = nltk.sent_tokenize(text)
    if len(sents) <= 0:
        return None

    first_sent = (nltk.sent_tokenize(text)[0]).encode('utf-8').strip()
    return first_sent

def get_expl_and_entities(title_and_body):
    wikitext = title_and_body[1]
    title = title_and_body[0]
    links = get_links(wikitext)

    explanation = get_first_sentence(title)
    if explanation == None:
        return None

    entities = []

    for link in links:
        if link in explanation:
            entities.append(link)

    if not entities:
        return None

    return explanation, entities
