import scrapy
from scrapy.http import Response

from config import TECHNOLOGIES, ENGLISH


class VacanciesSpider(scrapy.Spider):
    name = "vacancies_spider"
    allowed_domains = ["djinni.co"]
    start_urls = [
        "https://djinni.co/jobs/?primary_keyword=Python"
    ]

    def parse(self, response: Response, **kwargs):
        for vacancy in response.css(".job-list-item"):
            url = vacancy.css("a.h3::attr(href)").get()
            yield response.follow(url, self.parse_vacancy)

        next_page = response.css(
            "li.page-item:last-child a.page-link::attr(href)"
        ).get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_vacancy(self, vacancy: Response):
        yield {
            "title": vacancy.css("h1::text").get().strip(),
            "stack": VacanciesSpider.get_stack(
                vacancy.css(
                    ".col-sm-8"
                ).get().lower()
            ),
            "salary": VacanciesSpider.get_salary(vacancy),
            "english_level": VacanciesSpider.get_english_level(vacancy),
            "experience_years": VacanciesSpider.get_experience_years(vacancy),
            "reviews_count": int(vacancy.css(
                "p.text-muted"
            ).extract_first().split()[-3]),
            "url": vacancy.url
        }

    @staticmethod
    def get_stack(text: str) -> list:

        return list({tech for tech in TECHNOLOGIES if tech.lower() in text.lower()})

    @staticmethod
    def get_experience_years(response: Response) -> int:
        exp_text = response.css(".job-additional-info--body li:last-child div::text").get()
        if "No experience" in exp_text:
            experience_years = 0
        else:
            experience_years = int(exp_text.split()[0].strip().replace("No experience", "0"))

        return experience_years

    @staticmethod
    def get_english_level(response: Response) -> str:
        lvl = response.css(
                ".job-additional-info--item-text:contains('Англійська')::text"
            ).get().strip()
        return ENGLISH.index(" ".join(lvl.split()[1:]))

    @staticmethod
    def get_salary(response: Response) -> str:
        salary = response.css(
            "header .public-salary-item::text"
        ).get()
        if salary is not None:
            return salary.strip()


