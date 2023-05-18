from dataclasses import dataclass


@dataclass
class InputTextEng:
    pack_price_pharmacy_label: str = 'Pack price in pharmacy, Rubs with VAT'
    pack_price_pharmacy_help: str = 'Enter the final price in Rubs for the buyer'
    pack_price_manufacturer_label: str = 'Purchase price from the manufacturer, Rubs without VAT'
    pack_price_manufacturer_help: str = 'Purchase price from the manufacturer'
    pack_price_owner_label: str = 'Purchase price from the owner, Rubs without VAT'
    pack_price_owner_help: str = 'Purchase price from the manufacturer'
    pack_price_change_label: str = 'Change of pharmacy price, %'
    pack_price_change_help: str = 'Choose pack price change'


@dataclass
class InputTextRus:
    pack_price_pharmacy_label: str = 'Цена в аптеке, руб. с НДС'
    pack_price_pharmacy_help: str = 'Конечная цена одной упаковки для розничного покупателя в аптеке, рублей с НДС'
    pack_price_manufacturer_label: str = 'Себестоимость, руб. без НДС'
    pack_price_manufacturer_help: str = 'Цена закупки одной упаковки у завода производителя, рублей без НДС'
    pack_price_owner_label: str = 'Отгрузка в аптеку, руб. без НДС'
    pack_price_owner_help: str = 'Цена одной упаковки при отгрузке в аптеку, рублей без НДС'
    pack_price_change_label: str = 'Изменение цены для аптеки, %'
    pack_price_change_help: str = 'Изменение цены отгрузки одной упаковки **от владельца в аптеку**'
    salary_label: str = 'Оклад'
    salary_help: str = 'Оклад'
    compensation_label: str = 'Представ. расходы'
    compensation_help: str = 'Компенсируемые ежемесячные расходы'
    quarter_bonus_label: str = 'Q бонус, %'
    quarter_bonus_help: str = 'Квартальный бонус'
    year_bonus_label: str = 'Y бонус, %'
    year_bonus_help: str = 'Годовой бонус'
    tax_type_label: str = 'Налоги'
    tax_type_help: str = 'Тип налогообложения'


tm = InputTextRus()
months_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']





online_salary_condition = {
    'MarketingSp': {
        'salary': 150_000,
        'bonus': 30,
        'tax_index': 0,
        'fullname': 'Marketing Specialist',
        'fullname_rus': 'Маркетолог',
        'shortname': 'online_ms'},
    'PRT_Dir': {
        'salary': 500_000,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'PRT Direct',
        'fullname_rus': 'PRT - Директ',
        'shortname': 'online_prt_dir'},
    'PRT_Dev': {
        'salary': 300_000,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'PRT Development Specialist',
        'fullname_rus': 'PRT - Разработка и поддержание сайта',
        'shortname': 'online_prt_dev'},
    'Reputation': {
        'salary': 0,
        'bonus': 0,
        'tax_index': 1,
        'fullname': 'Reputation',
        'fullname_rus': 'Репутация',
        'shortname': 'online_rep'},
}

online_source = {
    'Yandex': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Yandex',
        'shortname': 'yandex',
    },
    'VK': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Вконтакте',
        'shortname': 'vk',
    },
    'OK': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Одноклассники',
        'shortname': 'ok',
    },
    'Instagram': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'Инстаграмм (экстремистская орг.)',
        'shortname': 'insta',
    },
    'YouTube': {
        'monthly_cost': 100_000,
        'audience_coverage': 10_000,
        'conversion': 10,
        'fullname': '',
        'fullname_rus': 'YouTube',
        'shortname': 'youtube',
    }
}
