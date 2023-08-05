import re
from typing import Union, Dict, Sequence

import js2py
import js2py.internals.simplex
import numpy
import pandas
import parsel

from extreme_parser.amazon.product.model import Product
from extreme_parser.util.parse import parse_number


def table(selector: parsel.Selector, exp: str, *fields) -> str:
    tbl = selector.xpath(exp).get()
    if tbl is None:
        return ""
    tbl = pandas.read_html(tbl)
    if len(tbl) <= 0:
        return ""
    tbl = tbl[0].set_index(0)

    for f in fields:
        if f in tbl[1]:
            return tbl[1][f]
    else:
        return ""


def tabular_buy_box_container(selector: parsel.Selector, *fields) -> str:
    return table(selector, "//table[@id='tabular-buybox-container']", *fields)


def product_overview_feature_div(selector: parsel.Selector, *fields) -> str:
    return table(selector, "//div[@id='productOverview_feature_div']//table", *fields)


def product_details_detail_bullets(selector: parsel.Selector, *fields) -> str:
    return table(selector, "//table[@id='productDetails_detailBullets_sections1']", *fields)


def product_details_tech_spec(selector: parsel.Selector, *fields) -> str:
    return table(selector, "//table[@id='productDetails_techSpec_section_1']", *fields)


def parse(html: str, p: Product, include: Sequence = None):
    include = include or Product.__fields__.keys()

    def should_price():
        return "price_min" in include or "price_max" in include

    def should_ship_day():
        return "ship_day_min" in include or "ship_day_max" in include

    def should_size():
        return "size_length" in include or "size_width" in include or "size_height" in include

    def should_variation():
        return "variation_values" in include or "selected_variations" in include or "asin_variation_values" in include

    def should_thumbnail():
        return "thumbnail" in include or "thumbnails" in include

    sel = parsel.Selector(text=html)
    "parent_asin" in include and parse_parent_asin(p, selector=sel)
    "weight" in include and parse_weight(p, selector=sel)
    "brand" in include and parse_brand(p, selector=sel)
    should_price() and parse_price(p, selector=sel)
    "available" in include and parse_available(p, selector=sel)
    "in_stock" in include and parse_in_stock(p, selector=sel)
    "stock" in include and parse_stock(p, selector=sel)
    should_ship_day() and parse_ship_day(p, selector=sel)
    "ship" in include and parse_ship(p, selector=sel)
    "sold" in include and parse_sold(p, selector=sel)
    "sold_url_rel" in include and parse_sold_url_rel(p, selector=sel)
    "offers" in include and parse_offers(p, selector=sel)
    "delivery" in include and parse_delivery(p, selector=sel)
    "material" in include and parse_material(p, selector=sel)
    "description" in include and parse_description(p, selector=sel)
    "title" in include and parse_title(p, selector=sel)
    should_size() and parse_size(p, selector=sel)
    "color" in include and parse_color(p, selector=sel)
    should_variation() and parse_variation(p, selector=sel)
    "review_amount" in include and parse_review_amount(p, selector=sel)
    "review_star" in include and parse_review_star(p, selector=sel)
    "rank" in include and parse_rank(p, selector=sel)
    should_thumbnail() and parse_thumbnail(p, selector=sel)
    "category" in include and parse_category(p, selector=sel)
    "date_first_avail" in include and parse_date_first_avail(p, selector=sel)
    "customize" in include and parse_customize(p, html=html)
    "images" in include and parse_images(p, selector=sel)
    "aplus" in include and parse_aplus(p, selector=sel)


def parse_parent_asin(p: Product, selector: parsel.Selector = None):
    p.parent_asin = selector.re_first(r'"parentAsin":"(.+?)"')


def parse_weight(p: Product, selector: parsel.Selector = None):
    def s1() -> str:
        s = product_details_detail_bullets(selector, "Item Weight")
        s = s or product_details_tech_spec(selector, "Item Weight")
        return s

    def s2() -> str:
        ul = selector.xpath("//div[@id='detailBullets_feature_div']/ul")
        s = ul.xpath("//span[contains(text(), 'Item Weight')]/following-sibling::span[1]/text()").get()
        s = s or ul.xpath(
            "substring-after(//span[contains(text(), 'Product Dimensions')]/following-sibling::span[1]/text(), '; ')"
        ).get("")
        return s

    weight_str = s1() or s2()
    weight: Union[None, int, float] = parse_number(weight_str)
    if weight is None:
        p.weight = None
        return

    if weight_str.lower().endswith("ounces"):
        p.weight = round(weight * 0.0625, 2)
    elif weight_str.lower().endswith("pounds"):
        p.weight = round(float(weight), 2)
    else:
        p.weight = None


def parse_brand(p: Product, selector: parsel.Selector = None):
    def s1() -> str:
        return product_overview_feature_div(selector, "Brand")

    def s2() -> str:
        s = selector.xpath("//a[@id='bylineInfo']/text()").re_first(".*?: (.*)")
        s = s or selector.xpath("//a[@id='bylineInfo']/text()").re_first("Visit the (.*) Store")
        return s

    brand = s1() or s2()
    if brand == "":
        p.brand = None
        return

    p.brand = brand


def parse_price(p: Product, selector: parsel.Selector = None):
    def price_table() -> pandas.DataFrame:
        t = pandas.DataFrame(index=("origin", "discount"), columns=('title', 'price'))
        for i, tr in enumerate(selector.xpath("//div[@id='price']/table/tr")[:2]):
            t.iat[i, 0] = tr.xpath("normalize-space(./td[1]/text())").get()
            t.iat[i, 1] = tr.xpath("normalize-space(./td[2]/span[1]/text())").get()
        return t

    def s1() -> str:
        s = selector.xpath("//div[@id='buyNew_noncbb']/span/text()").get()
        s = s or selector.xpath("//*[@id='color_name_0_price']/span/text()[last()]").get()
        s = s or selector.xpath("//span[@id='sns-base-price']/text()").get()
        s = s or selector.xpath("//div[@id='olp_feature_div']//span[@class='a-size-base a-color-price']/text()").get()
        return s or ""

    def s2() -> str:
        t = price_table()
        if numpy.all(t["price"] == ""):
            price = ""
        elif numpy.any(t["price"] == ""):
            price = t["price"][t["price"] != ""][0]
        else:
            price = t.at["origin", "price"]
        return "" if pandas.isna(price) else str(price)

    prices_str = (s2() or s1()).strip()
    prices: Union[None, list] = parse_number(prices_str.replace(",", ""), first=False)
    if prices is None or len(prices) == 0:
        p.price_min = None
        p.price_max = None
    elif len(prices) == 1:
        p.price_min = None
        p.price_max = float(prices[0])
    else:
        p.price_min = float(prices[0])
        p.price_max = float(prices[1])


def parse_available(p: Product, selector: parsel.Selector = None):
    available = selector.xpath("//div[@id='availability']/span/text()").get()
    if available is None:
        p.available = None
        return

    available = available.strip()
    if available == "Currently unavailable.":
        p.available = False
    else:
        p.available = True


def parse_in_stock(p: Product, selector: parsel.Selector = None):
    in_stock = selector.xpath("//div[@id='availability']/span/text()").get()
    in_stock = in_stock or selector.xpath("//div[@id='availability-string']/span/text()").get()
    if in_stock is None:
        p.in_stock = None
        return

    in_stock = in_stock.strip().lower()
    if (
        in_stock == "in stock." or
        in_stock.startswith("only") or
        in_stock.startswith("usually") or
        in_stock.startswith("available")
    ):
        p.in_stock = True
    elif in_stock in ["in stock soon.", "currently unavailable.", "temporarily out of stock.", ""]:
        p.in_stock = False
    elif in_stock.startswith("this item will be released on"):
        p.in_stock = False
    else:
        p.in_stock = None


def parse_stock(p: Product, selector: parsel.Selector = None):
    stock = selector.xpath("//div[@id='availability']/span/text()").get()
    if stock is None:
        p.stock = None
        return
    stock = stock.strip()
    if not stock.startswith("Only"):
        p.stock = None
        return

    p.stock = parse_number(stock)


def parse_ship_day(p: Product, selector: parsel.Selector = None):
    ship_day = selector.xpath("//div[@id='availability']/span/text()").re(r"Usually ships within (\d+) to (\d+) days.")
    if len(ship_day) < 2:
        p.ship_day_min = None
        p.ship_day_max = None
    else:
        p.ship_day_min = int(ship_day[0])
        p.ship_day_max = int(ship_day[1])


def parse_ship(p: Product, selector: parsel.Selector = None):
    def s1() -> str:
        return tabular_buy_box_container(selector, "Ships from", "Dispatches from")

    def s2() -> str:
        ship = selector.xpath("normalize-space(//div[@id='sfsb_accordion_head']/div/div/span[2]/text())").get()
        return ship or ""

    def s3() -> str:
        ship_sel = selector.xpath("normalize-space(string(//div[@id='merchant-info']))")
        ship = ship_sel.re("Ships from and sold by (.+).$")
        ship = ship or ship_sel.re("Sold by .+? and Fulfilled by (.+).$")
        if len(ship) > 0:
            return ship[0]
        else:
            return ""

    ship_str = s1() or s2() or s3()
    if ship_str != "":
        p.ship = ship_str.lower()
    else:
        p.ship = None


def parse_sold(p: Product, selector: parsel.Selector = None):
    def s1() -> str:
        return selector.xpath("//a[@id='sellerProfileTriggerId']/text()").get("")

    def s2() -> str:
        text = selector.xpath("normalize-space(string(//div[@id='merchant-info']))")
        s = text.re_first(r"Ships from and sold by (.+)\.")
        s = s or text.re_first(r"Sold by (.+) and Fulfilled by")
        return s or ""

    sold = s1() or s2()
    if sold == "":
        p.sold = None
    else:
        p.sold = sold


def parse_sold_url_rel(p: Product, selector: parsel.Selector = None):
    sold_url_rel = selector.xpath("//a[@id='sellerProfileTriggerId']/@href").get()
    sold_url_rel = sold_url_rel or selector.xpath("//div[@id='merchant-info']/a/@href").get()
    if sold_url_rel is None:
        p.sold_url_rel = None
    else:
        p.sold_url_rel = sold_url_rel


def parse_offers(p: Product, selector: parsel.Selector = None):
    offers = selector.xpath(
        "//div[@id='olpLinkWidget_feature_div']//div[@class='olp-text-box']/span[1]/text()"
    ).get()
    if offers is None:
        p.offers = None
        return

    p.offers = parse_number(offers)


def parse_delivery(p: Product, selector: parsel.Selector = None):
    delivery = selector.xpath("string(//div[@id='contextualIngressPtLabel_deliveryShortLine'])").get()
    delivery = delivery or selector.xpath("normalize-space(//span[@id='glow-ingress-line2']/text())").get()
    if delivery is None or delivery == "":
        p.delivery = None
        return
    if delivery in ["Select delivery location", "Select your address"]:
        p.delivery = "local"
        return
    if not delivery.startswith("Deliver to"):
        p.delivery = None
        return

    delivery = re.search(r"Deliver to\s(.*)", delivery)
    if delivery is None:
        p.delivery = None
    else:
        p.delivery = delivery.group(1)


def parse_material(p: Product, selector: parsel.Selector = None):
    material = product_overview_feature_div(selector, "Material")
    if material == "":
        p.material = None
    else:
        p.material = material


def parse_description(p: Product, selector: parsel.Selector = None):
    texts = selector.xpath("//div[@id='feature-bullets']//li[not(@id)]/span/text()").getall()
    if len(texts) < 1:
        p.description = None
        return

    desc = list()
    for t in texts:
        desc.append(t.strip())
    p.description = desc


def parse_title(p: Product, selector: parsel.Selector = None):
    title = selector.xpath("normalize-space(//span[@id='productTitle']/text())").get()
    if title == "":
        p.title = None
    else:
        p.title = title


def parse_size(p: Product, selector: parsel.Selector = None):
    dimensions = product_details_detail_bullets(selector, "Product Dimensions", "Package Dimensions")
    dimensions = dimensions or product_details_tech_spec(selector, "Product Dimensions", "Package Dimensions")
    if not dimensions.endswith("inches"):
        p.size_length = None
        p.size_width = None
        p.size_height = None
        return

    dimensions = parse_number(dimensions, first=False)
    if len(dimensions) >= 3:
        p.size_length = str(dimensions[0]) + " in"
        p.size_width = str(dimensions[1]) + " in"
        p.size_height = str(dimensions[2]) + " in"
    elif len(dimensions) == 2:
        p.size_length = str(dimensions[0]) + " in"
        p.size_width = str(dimensions[1]) + " in"
        p.size_height = None
    elif len(dimensions) == 1:
        p.size_length = str(dimensions[0]) + " in"
        p.size_width = None
        p.size_height = None
    else:
        p.size_length = None
        p.size_width = None
        p.size_height = None


def parse_color(p: Product, selector: parsel.Selector = None):
    color = selector.xpath("normalize-space(string(//div[@id='prodDetails']/span))").re_first("Color:(.+?)(?: |$)")
    if color is None:
        p.color = None
    else:
        p.color = color.lower()


def parse_variation(p: Product, selector: parsel.Selector = None):
    variation = selector.xpath(
        "normalize-space(//script[contains(text(), 'twister-js-init-dpx-data')]/text())"
    ).re_first("dataToReturn = {.+};")
    if variation is None:
        p.variation_values = None
        p.selected_variations = None
        p.asin_variation_values = None
        return

    try:
        variation = js2py.eval_js(variation)
        labels = variation.variationDisplayLabels.to_dict()
        values = variation.variationValues.to_dict()
        selected = variation.selected_variations.to_dict()
        variations = variation.asinVariationValues.to_dict()
    except (js2py.internals.simplex.JsException, AttributeError, RuntimeError):
        p.variation_values = None
        p.selected_variations = None
        p.asin_variation_values = None
        return

    def change_key(d: dict):
        return {labels[k]: v for k, v in d.items() if k in labels}

    def change_variations(vars_ori: dict) -> Dict[str, dict]:
        vars_change = dict()
        for asin, var in vars_ori.items():
            var_change = dict()
            for k, v in var.items():
                if k in labels and k in values:
                    var_change[labels[k]] = values[k][int(v)]
                else:
                    var_change[k] = v
            vars_change[asin] = var_change
        return vars_change

    p.variation_values = change_key(values)
    p.selected_variations = change_key(selected)
    p.asin_variation_values = change_variations(variations)


def parse_review_amount(p: Product, selector: parsel.Selector = None):
    amount = selector.xpath("//span[@id='acrCustomerReviewText']/text()").get()
    if amount is None:
        p.review_amount = None
    else:
        p.review_amount = parse_number(amount)


def parse_review_star(p: Product, selector: parsel.Selector = None):
    star = selector.xpath("//span[@id='acrPopover']/@title").get()
    if star is None:
        p.review_star = None
    else:
        p.review_star = parse_number(star)


def parse_rank(p: Product, selector: parsel.Selector = None):
    def s1() -> str:
        return product_details_detail_bullets(selector, "Best Sellers Rank")

    def s2() -> str:
        return selector.xpath("normalize-space(string(//span[contains(text(), 'Best Sellers Rank')]/..))").get()

    rank = s1() or s2()
    if rank == "":
        p.rank = None
        return
    rank = re.sub(r"\(.*?\)", "", rank)
    rank = re.findall(r"([\d,]+) in ([^\d]+)", rank)
    if len(rank) == 0:
        p.rank = None
        return

    rank = {r[1].strip(): int(r[0].replace(",", ""))
            for r in rank
            if len(r) == 2 and r[0].replace(",", "").isdigit()}
    if len(rank) == 0:
        p.rank = None
    else:
        p.rank = rank


def parse_thumbnail(p: Product, selector: parsel.Selector = None):
    thumbnail = selector.xpath("//div[@id='altImages']//img/@src").getall()
    thumbnail = thumbnail or selector.xpath("//div[@id='imageBlockThumbs']//img/@src").getall()
    if len(thumbnail) < 1:
        p.thumbnail = None
        p.thumbnails = None
    else:
        p.thumbnail = thumbnail[0]
        p.thumbnails = list(filter(lambda t: "transparent-pixel" not in t, thumbnail))


def parse_category(p: Product, selector: parsel.Selector = None):
    category = selector.xpath("normalize-space(//div[@id='nav-subnav']//span[1]/text())").get()
    category = category or selector.xpath("//div[@id='nav-subnav']//img[1]/@alt").get()
    if category is None:
        p.category = None
    else:
        p.category = category


def parse_date_first_avail(p: Product, selector: parsel.Selector = None):
    date = product_details_detail_bullets(selector, "Date First Available")
    date = date or selector.xpath(
        "//div[@id='detailBullets_feature_div']//span[contains(text(), 'Date First Available')]/"
        "following-sibling::span[1]/text()"
    ).get()
    if date == "":
        p.date_first_avail = None
    else:
        p.date_first_avail = date


def parse_customize(p: Product, html: str = None):
    p.customize = "This product needs to be customized before adding to cart." in html


def parse_images(p: Product, selector: parsel.Selector = None):
    def l1() -> list:
        images_block = selector.re_first(r"'colorImages': { 'initial': (\[.*\])},")
        if images_block is None:
            return list()
        images_block = re.findall(r'"main":{.*?}', images_block)
        if len(images_block) == 0:
            return list()

        images_urls = list()
        for image in images_block:
            urls = re.findall(r'"(https.*?)"', image)
            if len(urls) > 0:
                images_urls.append(urls[-1])
        return images_urls

    def l2() -> list:
        return selector.re(r'"mainUrl":"(.*?)"')

    images = l1() or l2()
    if len(images) == 0:
        p.images = None
    else:
        p.images = images


def parse_aplus(p: Product, selector: parsel.Selector = None):
    p.aplus = len(selector.xpath("//*[@id='aplus']")) > 0
