import pickle
from nltk.tokenize import word_tokenize

# Gives positive or negative sentiment to text using pickled classifier
# .classify(text) method takes dictionary where keys are words as strings and values
# are bools (True or False) indicating whether to include word in analysis
# Call main() with either manually created dict or text file (see bottom for details)

def getClassifier(pickled_classifier_path):
    # Loads pickled classifier and returns classifier
        classifier_file = open(pickled_classifier_path, 'r')
            classifier = pickle.load(classifier_file)
                return classifier


                def convertStrToDict(text_str_path):
                    # Takes file path and returns dictionary where all of the
                        # text_str words are keys and values are True.

                            text_str = open(text_str_path, 'r').read().lower()
                                text_list = word_tokenize(text_str)
                                    return dict((word, True) for word in text_list)


                                    def getSentiment(classifier, text):
                                        # Takes classifier and string of text
                                            # Returns positive or negative sentiment
                                                # classifier.show_most_informative_features(10)
                                                    if type(text) == dict:
                                                                return classifier.classify(text)


                                                                def main(pickled_classifier_path, text, text_path):
                                                                    # Takes text as a dict or text_path of a text file and returns neg or pos sentiment
                                                                        classifier = getClassifier(pickled_classifier_path)
                                                                            if text_path:
                                                                                        text = convertStrToDict(text_path)
                                                                                            return getSentiment(classifier, text)

                                                                                            pickled_classifier_path = r'C:\work\script\pythonScripts\HotelRatings\data\hotelReviews\classifier.pickle'
                                                                                            text_path = r'C:\work\script\pythonScripts\HotelRatings\review_test.txt'
# text = {'bad': True, 'great': True, 'good': True}

# If manually entered text doesn't exist use text_path file
try:
    text
    except NameError:
        sentiment = main(pickled_classifier_path, None, text_path)
        else:
                sentiment = main(pickled_classifier_path, text, None)

                print sentiment


