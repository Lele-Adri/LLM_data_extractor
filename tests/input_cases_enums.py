from enum import Enum


class UrlSource(Enum):
    LOCAL_TEST  = ("",)
    GITHUB      = ("https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",)
    ATP         = ("https://www.atptour.com/en/rankings/singles",)
    BAIN        = ("https://www.baincapitalprivateequity.com/",)
    ITTF        = ("https://ranking.ittf.com/#/home",)
    INVALID_URL = ("someinvalidurlhere!",)

    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url


class SoughtData(Enum):
    PARTNER_PROFILE = (
        "profile of potential partners", 
        "Types of companies that have interesting profiles to partner with."
    )
    PRIMARY_AND_ADDON = (
        "primary and add-on investments", 
        "Number of primary and add-on investments done by the company."
    )
    AGE_KYRGIOS = (
        "age of Nick Kyrgios", 
        "The age of the tennis player Nick Kyrgios."
    )
    PERSONAL_DATA_COLLECTION = (
        "personal data collection", 
        "Information about the type of personal data collected by the company."
    )
    USE_OF_PERSONAL_DATA = (
        "use of personal data", 
        "Information about how github uses the collected personal data it's collecting."
    )
    COFOUNDERS = (
        "names of (co)founders", 
        "The name of the founders of the company."
    )
    AGE_NATIONALITY_NOVAK = (
        "Novack Djockovic age and nationality", 
        "The age and nationality of Novak Djockovic."
    )
    TOP_5_IN_RANKINGS = (
        "Top 5 players in the ranking", 
        "The name and nationality of the top 5 ranked players."
    )
    LIST_OF_SOCIAL_MEDIA_ACCOUNTS = (
        "List of social media accounts of the company", 
        "A list of the company's social media accounts listed on the website."
    )

    def __init__(self, name, description):
        self._name = name
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description