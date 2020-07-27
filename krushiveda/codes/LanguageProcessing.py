import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import random

from sklearn.naive_bayes import MultinomialNB



def get_plant_question_dataset():
    dataset = [["How to resolve Potato Early blight", "potato_early_blight"],
               ["How to resolve Potato Late blight", "potato_late_blight"],
               ["How to resolve Tomato Bacterial spot", "tomato_bacterial_spot"],
               ["How to resolve Tomato Early blight", "tomato_early_blight"],
               ["How to resolve Tomato Late Blight", "tomato_late_blight"],
               ["How to resolve Tomato Leaf Mold", "tomato_leaf_mold"],
               ["How to resolve Tomato Septoria Leaf Spot", "tomato_septoria_leaf_spot"],
               ["How to resolve Tomato Spider Mites Two Spotted Spider Mite", "tomato_spider_mites"],
               ["How to resolve Tomato Target Spot", "tomato_target_spot"],
               ["How to resolve Tomato YellowLeaf Curl Virus", "tomato_curl_virus"],
               ["How to resolve Tomato Mosaic Virus", "tomato_mosaic_virus"],

               ["How to cure Potato Early blight", "potato_early_blight"],
               ["How to cure Potato Late blight", "potato_late_blight"],
               ["How to cure Tomato Bacterial spot", "tomato_bacterial_spot"],
               ["How to cure Tomato Early blight", "tomato_early_blight"],
               ["How to cure Tomato Late Blight", "tomato_late_blight"],
               ["How to cure Tomato Leaf Mold", "tomato_leaf_mold"],
               ["How to cure Tomato Septoria Leaf Spot", "tomato_septoria_leaf_spot"],
               ["How to cure Tomato Spider Mites Two Spotted Spider Mite", "tomato_spider_mites"],
               ["How to cure Tomato Target Spot", "tomato_target_spot"],
               ["How to cure Tomato YellowLeaf Curl Virus", "tomato_curl_virus"],
               ["How to cure Tomato Mosaic Virus", "tomato_mosaic_virus"],

               ["What is Potato Early blight ?", "potato_early_blight_description"],
               ["What is Potato Late blight", "potato_late_blight_description"],
               ["What is Tomato Bacterial spot", "tomato_bacterial_spot_description"],
               ["What is Tomato Early blight", "tomato_early_blight_description"],
               ["What is Tomato Late Blight", "tomato_late_blight_description"],
               ["What is Tomato Leaf Mold", "tomato_leaf_mold_description"],
               ["What is Tomato Septoria Leaf Spot", "tomato_septoria_leaf_spot_description"],
               ["What is Tomato Spider Mites Two Spotted Spider Mite", "tomato_spider_mites_description"],
               ["What is Tomato Target Spot", "tomato_target_spot_description"],
               ["What is Tomato YellowLeaf Curl Virus", "tomato_curl_virus_description"],
               ["What is Tomato Mosaic Virus", "tomato_mosaic_virus_description"],

               ["What is Early blight on potatoes ?", "potato_early_blight_description"],
               ["What is Late blight on potatoes ?", "potato_late_blight_description"],
               ["What are Bacterial spot on tomatoes ?", "tomato_bacterial_spot_description"],
               ["What is Early blight on tomatoes ?", "tomato_early_blight_description"],
               ["What is Late Blight on tomatoes ?", "tomato_late_blight_description"],
               ["What are Leaf Mold on tomatoes ?", "tomato_leaf_mold_description"],
               ["What are Septoria Leaf Spot on tomatoes ?", "tomato_septoria_leaf_spot_description"],
               ["What are Spider Mites Two Spotted Spider Mite on tomatoes ?", "tomato_spider_mites_description"],
               ["What are Target Spot on tomatoes ?", "tomato_target_spot_description"],
               ["What are YellowLeaf Curl Virus on tomatoes ?", "tomato_curl_virus_description"],
               ["What are Mosaic Virus on tomatoes ?", "tomato_mosaic_virus_description"],

               ["What is the cure of Potato Early blight", "potato_early_blight"],
               ["What is the cure of Potato Late blight", "potato_late_blight"],
               ["What is the cure of Tomato Bacterial spot", "tomato_bacterial_spot"],
               ["What is the cure of Tomato Early blight", "tomato_early_blight"],
               ["What is the cure of Tomato Late Blight", "tomato_late_blight"],
               ["What is the cure of Tomato Leaf Mold", "tomato_leaf_mold"],
               ["What is the cure of Tomato Septoria Leaf Spot", "tomato_septoria_leaf_spot"],
               ["What is the cure of Tomato Spider Mites Two Spotted Spider Mite", "tomato_spider_mites"],
               ["What is the cure of Tomato Target Spot", "tomato_target_spot"],
               ["What is the cure of Tomato YellowLeaf Curl Virus", "tomato_curl_virus"],
               ["What is the cure of Tomato Mosaic Virus", "tomato_mosaic_virus"],

               ["Describe Potato Early blight to me", "potato_early_blight_description"],
               ["Describe Potato Late blight to me", "potato_late_blight_description"],
               ["Describe Tomato Bacterial spot to me", "tomato_bacterial_spot_description"],
               ["Describe Tomato Early blight to me", "tomato_early_blight_description"],
               ["Describe Tomato Late Blight to me", "tomato_late_blight_description"],
               ["Describe Tomato Leaf Mold to me", "tomato_leaf_mold_description"],
               ["Describe Tomato Septoria Leaf Spot to me", "tomato_septoria_leaf_spot_description"],
               ["Describe Tomato Spider Mites Two Spotted Spider Mite to me",
                "tomato_spider_mites_description"],
               ["Describe Tomato Target Spot to me", "tomato_target_spot_description"],
               ["Describe Tomato YellowLeaf Curl Virus to me", "tomato_curl_virus_description"],
               ["Describe Tomato Mosaic Virus to me", "tomato_mosaic_virus_description"],

               ["Tell me something about Potato Early blight", "potato_early_blight_description"],
               ["Tell me something about Potato Late blight", "potato_late_blight_description"],
               ["Tell me something about Tomato Bacterial spot", "tomato_bacterial_spot_description"],
               ["Tell me something about Tomato Early blight", "tomato_early_blight_description"],
               ["Tell me something about Tomato Late Blight", "tomato_late_blight_description"],
               ["Tell me something about Tomato Leaf Mold", "tomato_leaf_mold_description"],
               ["Tell me something about Tomato Septoria Leaf Spot", "tomato_septoria_leaf_spot_description"],
               ["Tell me something about Tomato Spider Mites Two Spotted Spider Mite",
                "tomato_spider_mites_description"],
               ["Tell me something about Tomato Target Spot", "tomato_target_spot_description"],
               ["Tell me something about Tomato YellowLeaf Curl Virus", "tomato_curl_virus_description"],
               ["Tell me something about Tomato Mosaic Virus", "tomato_mosaic_virus_description"]
               ]
    dataset = pd.DataFrame(dataset, columns=["Text", "Category"])
    return dataset


def refine_dataset(dataset):

    lemmatizer = WordNetLemmatizer()

    for index, row in dataset.iterrows():
        text = row['Text'].lower()

        words = word_tokenize(text)

        words = [word for word in words if word.isalpha()]

        # Added Extra
        words = [lemmatizer.lemmatize(words[i], wordnet.VERB) for i in range(len(words))]
        words = [lemmatizer.lemmatize(words[i], wordnet.ADJ) for i in range(len(words))]
        words = [lemmatizer.lemmatize(words[i], wordnet.ADV) for i in range(len(words))]
        # till here...

        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        text = ' '.join(word for word in words)

        dataset.at[index, 'Text'] = text

    return dataset


def refine_test_text(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    words = text.split()

    # words = [word for word in words if word.isalpha()]

    # Added Extra
    words = [lemmatizer.lemmatize(words[i], wordnet.VERB) for i in range(len(words))]
    words = [lemmatizer.lemmatize(words[i], wordnet.ADJ) for i in range(len(words))]
    words = [lemmatizer.lemmatize(words[i], wordnet.ADV) for i in range(len(words))]
    # till here...

    # stop_words = set(stopwords.words('english'))
    # words = [w for w in words if not w in stop_words]

    text = ' '.join(word for word in words)

    return text


class LanguageProcessing:

    def __init__(self):
        self.dataset = get_plant_question_dataset()
        self.dataset = refine_dataset(self.dataset)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.dataset['Text'],
                                                                                self.dataset['Category'], test_size=0.2,
                                                                                random_state=32)

    def train_model(self):
        self.cv = CountVectorizer(max_features=1500)
        self.cv.fit(self.X_train)

        self.X_train_cv = self.cv.transform(self.X_train)

        self.X_test_cv = self.cv.transform(self.X_test)

        self.mnb = MultinomialNB(alpha=1)
        self.mnb.fit(self.X_train_cv, self.y_train)

    def get_model_accuracy(self):
        y_mnb = self.mnb.predict(self.X_test_cv)
        score = accuracy_score(y_mnb, self.y_test) * 100
        return score

    def predict_text_class(self, text):
        text = refine_test_text(text)
        doc = [text]
        sample_test = self.cv.transform(doc)
        return self.mnb.predict(sample_test)[0]