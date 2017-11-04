from .base_meta import MetaData


class PinterestMeta(MetaData):
    SEARCH_LINK = 'https://www.pinterest.ca/search/pins/?q={}'
    USER_LINK = 'https://www.pinterest.ca/{}/pins/'
    CATEGORY_LINK = 'https://www.pinterest.ca/categories/{}/'
