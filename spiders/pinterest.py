from .spiderling import Spiderling
import uuid


class Pinterest(Spiderling):
    QUALITY_MAPPING = {
        'small': '236x',
        'normal': '564x',
        'best': '736x'
    }

    def run(self):
        for element in self._queue:
            quality = self.QUALITY_MAPPING.get(self._quality, '564x')
            image = {
                'link': element['src'].replace('236x', quality),
                'title': element['alt'] if element.get('alt') else uuid.uuid4().hex,
                'format': 'jpg'
            }

            self.download(image)
