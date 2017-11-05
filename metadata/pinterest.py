from .base_meta import MetaData


class PinterestMeta(MetaData):
    SEARCH_LINK = 'https://www.pinterest.ca/search/pins/?q={}'
    USER_LINK = 'https://www.pinterest.ca/{}/pins/'
    CATEGORY_LINK = 'https://www.pinterest.ca/categories/{}/'
    RESOURCE_SELECTOR = 'img'
    RESOURCE_ATTR = 'src'
    NEXT_LEVEL_SELECTOR = 'div.GrowthUnauthPinImage > a'
    NEXT_LEVEL_ATTR = 'href'
