from .spiderling import Spiderling
import hashlib


class Pinterest(Spiderling):
    QUALITY_MAPPING = {
        'small': '/236x/',
        'normal': '/564x/',
        'best': '/736x/'
    }

    def run(self):
        for element in self._queue:
            quality = self.QUALITY_MAPPING.get(self._quality, '/564x/')
            link = element['src'].replace('/236x/', quality)
            image = {
                'link': link,
                'title': hashlib.sha256(link.encode('utf-8')).hexdigest(),
                'format': 'jpg'
            }

            self.download(image)
