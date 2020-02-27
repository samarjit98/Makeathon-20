import nltk
from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()

training_data = []
training_data.append({"class":"work", "sentence":"Meeting at 2 PM"})
training_data.append({"class":"work", "sentence":"Come to work early"})
training_data.append({"class":"work", "sentence":"Project starts from 10 AM"})
training_data.append({"class":"work", "sentence":"Client issue not solved"})
training_data.append({"class":"work", "sentence":"you are fired"})
training_data.append({"class":"work", "sentence":"you are hired"})
training_data.append({"class":"work", "sentence":"get it done by midnight"})
training_data.append({"class":"work", "sentence":"boss is angry"})
training_data.append({"class":"work", "sentence":"get that report"})
training_data.append({"class":"work", "sentence":"team coordination is of utmost importance"})
training_data.append({"class":"work", "sentence":"call me asap"})
training_data.append({"class":"work", "sentence":"need to talk"})
training_data.append({"class":"work", "sentence":"come to my office"})
training_data.append({"class":"work", "sentence":"do the tasks by today"})
training_data.append({"class":"work", "sentence":"write the code"})
training_data.append({"class":"work", "sentence":"give the presentation"})
training_data.append({"class":"work", "sentence":"talk to the HR"})
training_data.append({"class":"work", "sentence":"why are you late?"})
training_data.append({"class":"work", "sentence":"you got your promotion"})
training_data.append({"class":"work", "sentence":"no diwali bonus"})
training_data.append({"class":"work", "sentence":"get some interns"})
training_data.append({"class":"work", "sentence":"you got the promotion"})
training_data.append({"class":"work", "sentence":"you can't come late"})


training_data.append({"class":"home", "sentence":"Son failed at school"})
training_data.append({"class":"home", "sentence":"Bring vegetables while coming back"})
training_data.append({"class":"home", "sentence":"in laws coming today"})
training_data.append({"class":"home", "sentence":"my parents are ill"})
training_data.append({"class":"home", "sentence":"family problems father is ill"})
training_data.append({"class":"home", "sentence":"how was school today?"})
training_data.append({"class":"home", "sentence":"what do you want to have for dinner today?"})
training_data.append({"class":"home", "sentence":"love you guys a lot"})
training_data.append({"class":"home", "sentence":"kids do your homework"})
training_data.append({"class":"home", "sentence":"get it fixed by the plumber"})
training_data.append({"class":"home", "sentence":"i love you mom"})
training_data.append({"class":"home", "sentence":"i love you dad"})
training_data.append({"class":"home", "sentence":"i miss you parents"})
training_data.append({"class":"home", "sentence":"get the car from garage"})
training_data.append({"class":"home", "sentence":"we'll eat outside"})
training_data.append({"class":"home", "sentence":"good night babe"})
training_data.append({"class":"home", "sentence":"dinner is ready"})
training_data.append({"class":"home", "sentence":"call the plumber"})


training_data.append({"class":"travel", "sentence":"tickets have been booked"})
training_data.append({"class":"travel", "sentence":"flight has been cancelled"})
training_data.append({"class":"travel", "sentence":"train is on time"})
training_data.append({"class":"travel", "sentence":"bus service is really good"})
training_data.append({"class":"travel", "sentence":"lets go south"})
training_data.append({"class":"travel", "sentence":"lets plan a trip on car"})
training_data.append({"class":"travel", "sentence":"need to catch that train"})
training_data.append({"class":"travel", "sentence":"hotels have been booked"})
training_data.append({"class":"travel", "sentence":"get a good hotel"})
training_data.append({"class":"travel", "sentence":"lets go for some sightseeing"})
training_data.append({"class":"travel", "sentence":"look at that skyscraper"})
training_data.append({"class":"travel", "sentence":"hey what plans for vacation"})
training_data.append({"class":"travel", "sentence":"let's go"})
training_data.append({"class":"travel", "sentence":"vacations"})
training_data.append({"class":"travel", "sentence":"airports"})
training_data.append({"class":"travel", "sentence":"jetlag"})
training_data.append({"class":"travel", "sentence":"airline tickets"})
training_data.append({"class":"travel", "sentence":"travel agency"})
training_data.append({"class":"travel", "sentence":"trip"})
training_data.append({"class":"travel", "sentence":"hotels"})
training_data.append({"class":"travel", "sentence":"stomach is upset"})
training_data.append({"class":"travel", "sentence":"happy journey babe"})


training_data.append({"class":"spam", "sentence":"buy a credit card"})
training_data.append({"class":"spam", "sentence":"having a spam today?"})
training_data.append({"class":"spam", "sentence":"what's for lunch?"})
training_data.append({"class":"spam", "sentence":"buy this sim"})
training_data.append({"class":"spam", "sentence":"sir i want to apply for an internship"})
training_data.append({"class":"spam", "sentence":"hey beautiful wanna hang out?"})
training_data.append({"class":"spam", "sentence":"get this offer"})
training_data.append({"class":"spam", "sentence":"hey wassup"})
training_data.append({"class":"spam", "sentence":"cool offer coming up here"})
training_data.append({"class":"spam", "sentence":"STFU"})
training_data.append({"class":"spam", "sentence":"won money"})
training_data.append({"class":"spam", "sentence":"wanna make friendship"})
training_data.append({"class":"spam", "sentence":"earn money quick"})
training_data.append({"class":"spam", "sentence":"invest in mutual fund"})
training_data.append({"class":"spam", "sentence":"this is the best offer possible"})
training_data.append({"class":"spam", "sentence":"heavy discount"})
training_data.append({"class":"spam", "sentence":"free hotels"})

#print ("%s sentences of training data" % len(training_data))

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1
  # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])


# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
#print ("Class words: %s" % class_words)

def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1

            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score

def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score


#print (classify("family issue"))
