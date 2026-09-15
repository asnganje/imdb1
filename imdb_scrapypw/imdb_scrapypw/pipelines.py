# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import gspread
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
            "Name",
            "Director",
            "Year",
            "Duration",
            "Stars",
            "Votes",
            "Metascore",
            "Description"
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
    s_sheet_title = "imdbscraper output"
    w_sheet_title = "Movies"
    def open_spider(self, spider):
        credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")
        authorized_user_path = os.path.join(os.path.dirname(__file__), "authorized_user.json", )

        self.gc = gspread.oauth(
            credentials_filename=credentials_path,
            authorized_user_filename=authorized_user_path,
        )

        try:
            self.spreadsheet = self.gc.open(
                self.s_sheet_title
            )
        except gspread.exceptions.SpreadsheetNotFound:
            self.spreadsheet = self.gc.create(
                self.s_sheet_title
            )
            self.worksheet = self.spreadsheet.sheet1
            self.worksheet.update_title(self.w_sheet_title)
        else:
            try:
                self.worksheet = self.spreadsheet.worksheet(
                self.w_sheet_title)
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(title=self.w_sheet_title, rows=1100, cols=9, )
        headers = [
                "S/NO",
                "NAME",
                "DIRECTOR",
                "YEAR",
                "DURATION",
                "STARS",
                "VOTES",
                "METASCORE",
                "DESCRIPTION"
            ]
        if not self.worksheet.row_values(1):
            self.worksheet.append_row(headers)
        self.worksheet.format(
            "A1:I1",
            {
                "textFormat":{
                    "bold": True
                }
            }
        )
        self.serial = 1

    def process_item(self, item, spider):
        self.worksheet.append_row([
            self.serial,
            item['name'],
            item['director'],
            item['year'],
            item['duration'],
            item['stars'],
            item['votes'],
            item['metascore'],
            item['description']
        ])
        self.serial += 1
        return  item




