import json
from operator import itemgetter
import os
from dotenv import load_dotenv
from typing import Dict
import html2text
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import PromptTemplate
import htmlmin
from pydantic import HttpUrl

async def extract_information_from_html(html_content: str, data_to_extract: Dict[str, str]) -> Dict[str, str]:
    load_dotenv()

    # TODO: move this into some shared func
    llm = ChatOpenAI(
        temperature=0.1,
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        verbose=True,
        max_tokens=1000,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    sanitized_html = sanitize_html(html_content)
    prompt_string = get_prompt_as_template_string(sanitized_html, data_to_extract)
    # prompt_template = PromptTemplate.from_template(template=prompt_string)
    # formatted_prompt = prompt_template.format(html_content=html_content, data_to_extract=data_to_extract)
    # response = llm.invoke(formatted_prompt)
    response = llm.invoke(prompt_string)
    print(response)
    return { "top 5 players": "Nadal, Federer" }

def sanitize_html(html_content: str) -> str:
    html_content = htmlmin.minify(html_content, remove_comments=True, remove_empty_space=True)
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    html_content = converter.handle(html_content)

    return html_content.replace("{", "{{").replace("}", "}}")

# TODO: move somewhere and make a generic way to use across all files using langchain
# TODO: maybe put partial prompts in files (or just variables..)
def get_prompt_as_template_string(html_content, data_to_extract) -> str:
    example_section = get_extraction_prompt_example_html()
    sought_data_str = '\n'.join(f"\t\t'{key}': {value}" for key, value in data_to_extract.items())
    return f"""
[CONTEXT]
We are interested in extracting a series of information from the downloaded html content of a webpage.
[END CONTEXT]

[TASK]
We have some HTML content and a list with information we want to extract from it. 
Your task is to return a list with each element of the list and the corresponding extracted data from the HTML content.
[END TASK]

[EXAMPLE]
{example_section}
[END EXAMPLE]

From the presented HTML content, extract the following information:
{sought_data_str}

[HTML CONTENT]
{html_content}
[END HTML CONTENT]
    """
def get_extraction_prompt_example() -> str:
    return """
## EXAMPLE 1:
For the following html content
        <div class="row rackets-container"> <div class="wishlist-icon"> <div class="add-to-wishlist" data-pid="00906602938000" title="Ajouter à la liste de souhaits"></div> </div> <div class="col-md-6 image-container"> <div class="icons-and-badges"> <div class="badges"> <div class="product-badge sale">Promo -10%</div> </div> <div class="icons"> </div> </div> <div class="product-main-image" data-url="/on/demandware.store/Sites-TPO-FR-Site/fr_FR/Product-Variation" data-color-id="00906602938000" data-pid="00906602938000"> <a href="/babolat-boost-rafa-00906602938000.html"> <picture> <source media="(min-width: 1310px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=210" width="210" height="210"> <source media="(min-width: 1064px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=160" width="160" height="160"> <source media="(min-width: 769px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150" width="150" height="150"> <source media="(min-width: 540px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=180" width="180" height="180"> <img loading="lazy" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150 768w" alt="Raquettes De Tennis Babolat BOOST RAFA2 STRUNG" itemprop="image"> </picture> </a> </div> </div> <div class="col-md-6 attributes-container"> <div class="brand-icon-container"> <img class="brand-icon" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Library-Sites-TennisPoint/default/dw818bdcc0/brands/babolat.png?sw=50&amp;q=80" alt="Babolat"> </div> <div class="product-type-container"> <div class="product-type">Raquette polyvalentes</div> </div> <div class="product-description truncate-multiline" data-truncate-lines="2" itemprop="name" style="height: 42px;"> <a class="link" href="/babolat-boost-rafa-00906602938000.html" itemprop="url" title="Raquettes De Tennis Babolat Boost Rafa"> Boost Rafa </a> </div> <div class="price-highlight"> <div class="row price tiered-prices no-gutters"> <div class="col col-md-12 col-lg" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer"> <meta itemprop="priceCurrency" content="EUR"> <link itemprop="availability" href="http://schema.org/OutOfStock"> <link itemprop="itemCondition" href="http://schema.org/NewCondition"> <span class="list-sale-container"> <span class="strike-through list"> <span class="value"> 119,95 € </span> </span> <span class="sales" data-price-value="107.95"> <span class="value" itemprop="price" content="107.95"> 107,95 € </span> </span> </span> </div> </div> </div> <div class="ratings"> <div data-bv-show="inline_rating" data-bv-productid="00906602938000" data-bv-seo="false" data-bv-redirect-url="/babolat-boost-rafa-00906602938000.html"></div> </div> <div class="main-attributes"> <div class="attribute-values"> <div class="icon icons-headsize" title="Tamis (cm²)"></div> <span class="attribute-values-value">660 cm²</span> </div> <div class="attribute-values"> <div class="icon icons-stringpattern" title="Plan de cordage"></div> <span class="attribute-values-value">16/19</span> </div> <div class="attribute-values"> <div class="icon icons-weightunstrung" title="Poids non cordée (gr)"></div> <span class="attribute-values-value">260 g</span> </div> </div> <div class="product-compare form-group custom-control custom-checkbox" data-compare-pid="00906602938000"> <input class="custom-control-input" type="checkbox" id="00906602938000" value="true"> <label class="custom-control-label" for="00906602938000">Comparer</label> </div> </div> </div>
We want to extract:
    - 'Name of racket': The name of the racket.
    - 'Price of racket': The price of the racket.
### EXPECTED OUTPUT FOR EXAMPLE 1:
    - 'Name of racket': Boost Rafa
    - 'Price of racket': 107.09 euros.
## EXAMPLE 1:
For the following html content
        <div class="row rackets-container"> <div class="wishlist-icon"> <div class="add-to-wishlist" data-pid="00906602938000" title="Ajouter à la liste de souhaits"></div> </div> <div class="col-md-6 image-container"> <div class="icons-and-badges"> <div class="badges"> <div class="product-badge sale">Promo -10%</div> </div> <div class="icons"> </div> </div> <div class="product-main-image" data-url="/on/demandware.store/Sites-TPO-FR-Site/fr_FR/Product-Variation" data-color-id="00906602938000" data-pid="00906602938000"> <a href="/babolat-boost-rafa-00906602938000.html"> <picture> <source media="(min-width: 1310px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=210" width="210" height="210"> <source media="(min-width: 1064px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=160" width="160" height="160"> <source media="(min-width: 769px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150" width="150" height="150"> <source media="(min-width: 540px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=180" width="180" height="180"> <img loading="lazy" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150 768w" alt="Raquettes De Tennis Babolat BOOST RAFA2 STRUNG" itemprop="image"> </picture> </a> </div> </div> <div class="col-md-6 attributes-container"> <div class="brand-icon-container"> <img class="brand-icon" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Library-Sites-TennisPoint/default/dw818bdcc0/brands/babolat.png?sw=50&amp;q=80" alt="Babolat"> </div> <div class="product-type-container"> <div class="product-type">Raquette polyvalentes</div> </div> <div class="product-description truncate-multiline" data-truncate-lines="2" itemprop="name" style="height: 42px;"> <a class="link" href="/babolat-boost-rafa-00906602938000.html" itemprop="url" title="Raquettes De Tennis Babolat Boost Rafa"> Boost Rafa </a> </div> <div class="price-highlight"> <div class="row price tiered-prices no-gutters"> <div class="col col-md-12 col-lg" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer"> <meta itemprop="priceCurrency" content="EUR"> <link itemprop="availability" href="http://schema.org/OutOfStock"> <link itemprop="itemCondition" href="http://schema.org/NewCondition"> <span class="list-sale-container"> <span class="strike-through list"> <span class="value"> 119,95 € </span> </span> <span class="sales" data-price-value="107.95"> <span class="value" itemprop="price" content="107.95"> 107,95 € </span> </span> </span> </div> </div> </div> <div class="ratings"> <div data-bv-show="inline_rating" data-bv-productid="00906602938000" data-bv-seo="false" data-bv-redirect-url="/babolat-boost-rafa-00906602938000.html"></div> </div> <div class="main-attributes"> <div class="attribute-values"> <div class="icon icons-headsize" title="Tamis (cm²)"></div> <span class="attribute-values-value">660 cm²</span> </div> <div class="attribute-values"> <div class="icon icons-stringpattern" title="Plan de cordage"></div> <span class="attribute-values-value">16/19</span> </div> <div class="attribute-values"> <div class="icon icons-weightunstrung" title="Poids non cordée (gr)"></div> <span class="attribute-values-value">260 g</span> </div> </div> <div class="product-compare form-group custom-control custom-checkbox" data-compare-pid="00906602938000"> <input class="custom-control-input" type="checkbox" id="00906602938000" value="true"> <label class="custom-control-label" for="00906602938000">Comparer</label> </div> </div> </div>
We want to extract:
    - 'Founder name': The name of the founder of the website.
    - 'Contact address': The website's contact address.
### EXPECTED OUTPUT FOR EXAMPLE 1:
    - 'Founder name': 
    - 'Contact address': 
    """

def get_extraction_prompt_example_html() -> str:
    return """
<div class="col-12 ebw">
    <div class="row content-centered ebw">
        <div class="col ebw">
        <div class="row footer-legal-area ebw">
            <div class="col-12 col-md text-center text-md-left ebw">
                <div class="row no-gutters card-stop-area ebw">
                    <div class="col-12 col-md-3 ebw"><img src="/public/media/images/stopcard.png" class="card-stop-img ebw" alt="cardstop"></div>
                    <div class="col-sm-12 col-md card-stop-text d-sm-block ebw" hidden="">Carte perdue, volée ou avalée&nbsp;? <a href="tel:078%C2%A0170%C2%A0170" class="ebw">078&nbsp;170&nbsp;170</a></div>
                    <div class="col-12 card-stop-btn d-block d-sm-none ebw"><a href="tel:078%C2%A0170%C2%A0170" class="ebw"><span class="fontcon-phone-outline ebw"></span><span class="ebw">Carte perdue, volée ou avalée&nbsp;? </span></a></div>
                </div>
            </div>
            <div class="col-12 col-md text-center text-md-left ebw">
                <div class="row ebw">
                    <div class="col ebw">
                    <div class="sm-links-area d-sm-flex flex-sm-column ebw">
                        <p class="sm-links-title ebw">Social Links</p>
                        <div class="sm-links ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="https://www.facebook.com/BNPParibasFortisBelgique" target="_blank" class="fontcon-logo-facebook ebw"></a> <a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="https://twitter.com/BNPPFBelgique" target="_blank" class="fontcon-logo-twitter ebw"></a> <a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="https://linkedin.com/company/bnpparibasfortis" target="_blank" class="fontcon-logo-linkedin ebw"></a> <a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="https://www.youtube.com/bnppfBelgique" target="_blank" class="fontcon-logo-youtube ebw"></a> </div>
                    </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-6 text-center text-md-left ebw">
                <div class="row ebw">
                    <div class="col-12 col-md text-center legal-links text-md-left ebw">
                    <ul class="d-flex flex-wrap flex-column justify-content-start ebw">
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/a-propos-de-nous" class="ebw">À propos de nous</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/conditions-generales" class="ebw">Conditions générales</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/regles-conduites" class="ebw">Règles de conduite</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/liste-tarifs" class="ebw">Tarifs</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/particuliers/epargner-et-placer/protection-depots" class="ebw">Protection des dépôts</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/your-opinion-counts-fr" class="ebw">Suggestion ou plainte</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/particuliers/banque-au-quotidien/paiements/securite-en-ligne" class="ebw">Signaler une fraude</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/mention-legale" class="ebw">Conditions d'utilisation du site</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="#" data-topic="cc.policy.popup" data-data="" class="postPagebusMessage ebw">Cookies</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/vie-privee" class="ebw">Déclaration Vie Privée</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/us-policy" class="ebw">US Disclaimer</a></li>
                        <li class="ebw"><a xmlns:fn="http://www.w3.org/2005/xpath-functions" href="/fr/public/campagne/payment-services-directive" class="ebw">PSD2</a></li>
                    </ul>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</div>
    """

def get_extraction_prompt_actual_task(html_content: str, sought_data: Dict[str, str]) -> str:
    sought_data_str = '\n'.join(f"'\t\t{key}': {value}" for key, value in sought_data.items())
    return f"""
From the presented HTML content, extract the following information:
{sought_data_str}

[HTML CONTENT]
{html_content}
[END HTML CONTENT]
    """
def get_extraction_prompt_example() -> str:
    return """
For the following html content
        <div class="row rackets-container"> <div class="wishlist-icon"> <div class="add-to-wishlist" data-pid="00906602938000" title="Ajouter à la liste de souhaits"></div> </div> <div class="col-md-6 image-container"> <div class="icons-and-badges"> <div class="badges"> <div class="product-badge sale">Promo -10%</div> </div> <div class="icons"> </div> </div> <div class="product-main-image" data-url="/on/demandware.store/Sites-TPO-FR-Site/fr_FR/Product-Variation" data-color-id="00906602938000" data-pid="00906602938000"> <a href="/babolat-boost-rafa-00906602938000.html"> <picture> <source media="(min-width: 1310px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=210" width="210" height="210"> <source media="(min-width: 1064px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=160" width="160" height="160"> <source media="(min-width: 769px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150" width="150" height="150"> <source media="(min-width: 540px)" srcset="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=180" width="180" height="180"> <img loading="lazy" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0f5d9705/images/009/066/02938000_000.jpg?q=80&amp;sw=150 768w" alt="Raquettes De Tennis Babolat BOOST RAFA2 STRUNG" itemprop="image"> </picture> </a> </div> </div> <div class="col-md-6 attributes-container"> <div class="brand-icon-container"> <img class="brand-icon" src="https://www.tennis-point.fr/dw/image/v2/BBDP_PRD/on/demandware.static/-/Library-Sites-TennisPoint/default/dw818bdcc0/brands/babolat.png?sw=50&amp;q=80" alt="Babolat"> </div> <div class="product-type-container"> <div class="product-type">Raquette polyvalentes</div> </div> <div class="product-description truncate-multiline" data-truncate-lines="2" itemprop="name" style="height: 42px;"> <a class="link" href="/babolat-boost-rafa-00906602938000.html" itemprop="url" title="Raquettes De Tennis Babolat Boost Rafa"> Boost Rafa </a> </div> <div class="price-highlight"> <div class="row price tiered-prices no-gutters"> <div class="col col-md-12 col-lg" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer"> <meta itemprop="priceCurrency" content="EUR"> <link itemprop="availability" href="http://schema.org/OutOfStock"> <link itemprop="itemCondition" href="http://schema.org/NewCondition"> <span class="list-sale-container"> <span class="strike-through list"> <span class="value"> 119,95 € </span> </span> <span class="sales" data-price-value="107.95"> <span class="value" itemprop="price" content="107.95"> 107,95 € </span> </span> </span> </div> </div> </div> <div class="ratings"> <div data-bv-show="inline_rating" data-bv-productid="00906602938000" data-bv-seo="false" data-bv-redirect-url="/babolat-boost-rafa-00906602938000.html"></div> </div> <div class="main-attributes"> <div class="attribute-values"> <div class="icon icons-headsize" title="Tamis (cm²)"></div> <span class="attribute-values-value">660 cm²</span> </div> <div class="attribute-values"> <div class="icon icons-stringpattern" title="Plan de cordage"></div> <span class="attribute-values-value">16/19</span> </div> <div class="attribute-values"> <div class="icon icons-weightunstrung" title="Poids non cordée (gr)"></div> <span class="attribute-values-value">260 g</span> </div> </div> <div class="product-compare form-group custom-control custom-checkbox" data-compare-pid="00906602938000"> <input class="custom-control-input" type="checkbox" id="00906602938000" value="true"> <label class="custom-control-label" for="00906602938000">Comparer</label> </div> </div> </div>
We want to extract:
    - 'Name of racket': The name of the racket.
    - 'Price of racket': The price of the racket.
EXPECTED OUTPUT FOR EXAMPLE:
    - 'Name of racket': Boost Rafa
    - 'Price of racket': 107.09 euros.
    """