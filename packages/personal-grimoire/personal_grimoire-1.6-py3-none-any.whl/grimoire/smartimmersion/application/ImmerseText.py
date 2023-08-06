import logging

from pydantic import BaseModel

from grimoire.event_sourcing.message import MessageBroker
from grimoire.smartimmersion.config import ProductionSettings
from grimoire.smartimmersion.domain.paragraph import Paragraph
from grimoire.smartimmersion.domain.variations_generator.scored_variations import (
    ScoredVariations,
)


class ImmersedParagraph(BaseModel):
    query: str
    result: str
    domain: str
    headers: dict


class ImmerseText:
    def __init__(self):
        self.production_scored_variations = ScoredVariations(ProductionSettings)

    def immerse_web(self, query, request):
        result = self.immerse_paragraph(query)

        event = ImmersedParagraph(
            **{
                "query": query,
                "result": result,
                "headers": request.headers,
                "domain": request.headers.get("Origin", ""),
            }
        )
        MessageBroker("immersed_paragraphs").produce(event.dict())

        return result

    def immerse_paragraph(self, text):
        """
        Entry point for production
        """
        if not text or not len(text):
            logging.warning("Request to translate empty paragraph")
            return ""

        paragraph = Paragraph(text)
        sentences_immersed = []
        for sentence in paragraph.sentences:
            logging.info(f"Sentence to immerse {sentence.text}")

            try:
                immersed = self.production_scored_variations.get_for_sentence(sentence)[
                    0
                ].get_sentence()
                sentences_immersed.append(immersed)
            except Exception as e:
                logging.error(
                    "Exception happened while immersing sentence",
                    extra={"exception_as_str": str(e)},
                )

                sentences_immersed.append(sentence.text)

        result = ".".join(sentences_immersed)

        return result
