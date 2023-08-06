import os

API_PORT = 5007
dir_path = os.path.dirname(os.path.realpath(__file__))
# project root is the current directory
PROJECT_ROOT = dir_path


class ProductionSettings:
    """
    Settings that one might tunne differently while testing when compared with while running it on production"""

    manual_translations = {
        "of": "von",
        "more": "Mehr",
        "still": "noch",
        "listen": "horen",
        "is": "ist",
        "only": "nur",
        "their": "ihr",
        "usually": "normalerweise",
        "cannot": "kann_nicht",
        "are": "sind",
        "to": "zu",
        "at": "beim",
        "a": "ein",
        "on": "auf",
        "in": "im",
        "or": "oder",
        "an": "ein",
        "by": "durch",
        "about": "Über",
        "for": "zum",
        "can": "kann",
        "also": "ebenfalls",
        "my": "mein",
        "as": "wie",
        "it": "es",
        "he": "er",
        "people": "Menschen",
        "learn": "learnen",
        "time": "zeit",
    }

    DISABLE_TRANSLATIONS_API = True
    PERCENTAGE_OF_SENTENCES_TO_TRANSLATE = 100
    translations_percentages = [
        90,
        70,
        50,
        40,
        30,
        30,
        30,
        20,
        20,
        20,
        10,
        15,
        10,
    ]

    easy_words = [
        # define it lowercase
        "ein",
        "einen",
        "zu",
        "wort",
        "ohne",
        "ist",
        "nicht",
        "das",
        "von",
        "nein",
        "wir",
        "deutsche",
        "es",
        "im",
        "aber",
        "was",
        "gut",
        "welt",
        "jetz",
        "jetzt",
        "es",
        "viele",
        "sie",
        "und",
        "andere",
        "durch",
        "finger",
        "neu",
        "heute",
        "deutscheland",
        "letze",
        "sollte",
        "leben",
        "vielleicht",
    ]

    do_not_translate_words = [
        "weren't",
        "ultimately",
        "connected",
        "crave",
        "whatever",
        "they're",
        "that",
        "the",
        "are",
        "a",
        "their",
    ]


class TrainingSettings(ProductionSettings):
    DISABLE_TRANSLATIONS_API = False
    PERCENTAGE_OF_SENTENCES_TO_TRANSLATE = 50
    translations_percentages = [
        100,
        90,
        80,
        50,
        40,
        30,
        30,
        30,
        25,
        20,
        20,
        20,
        20,
        10,
        10,
        7,
        5,
        0,
    ]
