# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl.styles import Font
from openpyxl.workbook import Workbook


class ImdbScrapypwPipeline:
    def process_item(self, item):
        return item
class ExcelPipeline:
    def open_spider(self, spider):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "IMDBProducts"

        headers = [
            "S/No",
            "name",
            "director",
            "year",
            "duration",
            "stars",
            "votes",
            "metascore",
            "description"
        ]
        self.sheet.append(headers)
        for cell in self.sheet[1]:
            cell.font = Font(bold=True)
        self.serial_no = 1
    def process_item(self, item, spider):
        self.sheet.append([
            self.serial_no,
            item["name"],
            item["director"],
            item["year"],
            item["duration"],
            item["stars"],
            item["votes"],
            item["metascore"],
            item["description"]]
        )
        self.serial_no += 1
        return  item
    def close_spider(self, spider):
        self.workbook.save("movies.xlsx")
class GoogleSheetPipeline:
    s_sheet_title = "scraper output"
    w_sheet_title = "Movies"



