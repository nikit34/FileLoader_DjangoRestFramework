import xlrd, os
from django.conf import settings


class Sheet:
    def __init__(self, *args, **kwargs):
        self.media_path = ''

    def get_workbook(self, file):
        file_name = file.name
        if str(file_name[-5:]) == '.xlsx':
            self.media_path = str(settings.MEDIA_ROOT) + '/images/' + file_name
            workbook = xlrd.open_workbook(self.media_path)
            return workbook
        raise ValueError('Uncorrect format of file')

    @staticmethod
    def filter_int_cols(sheet, select):
        col_before = sheet.col_values(select['col_before'])
        col_after = sheet.col_values(select['col_after'])

        int_before = list(filter(lambda e: isinstance(e, float), col_before))
        int_after = list(filter(lambda e: isinstance(e, float), col_after))

        yield (int_before, int_after)


    def search_keys(workbook):
        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            select = {}
            for i_col in range(sheet.ncols):
                for i_row in range(sheet.nrows):
                    if sheet.cell_value(i_row, i_col) == 'before':
                        select['col_before'] = i_col
                        break
                    elif sheet.cell_value(i_row, i_col) == 'after':
                        select['col_after'] = i_col
                        break
                if 'col_after' in select and 'col_before' in select:
                    break
            yield (sheet, select)

    def find_number(l1, l2):
        for item_l1 in l1:
            for item_l2 in l2:
                if item_l1 == item_l2:
                    l1.remove(item_l1)
                    l2.remove(item_l1)
                    break
        return l1[0]

    @classmethod
    def proc(cls, file):
        result = {}
        workbook = cls.get_workbook(cls, file)
        for sheet, select in cls.search_keys(workbook):
            for before, after in cls.filter_int_cols(sheet, select):
                spred = len(before) - len(after)
                if spred == 1:
                    x = cls.find_number(before, after)
                    result['removed'] = x
                elif spred == -1:
                    x = cls.find_number(after, before)
                    result['added'] = x
                else:
                    raise ValueError('Going out of bounds')
        return result
