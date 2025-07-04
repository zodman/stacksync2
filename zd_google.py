import gspread
import os

GOOGLE_FILE_KEY = os.environ.get('GOOGLE_FILE_KEY')
GOOGLE_PAGE_ID = os.environ.get('GOOGLE_PAGE_ID')


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class WorksheetExists(Exception):
    pass


def _get_sheet():
    location_file = os.path.join(BASE_DIR, GOOGLE_FILE_KEY)
    gc = gspread.service_account(filename=location_file)
    sheet = gc.open_by_key(GOOGLE_PAGE_ID)

    return sheet


def _find_sheet_by_title(title):
    sheet = _get_sheet()
    list_worksheets = sheet.worksheets()
    for wsheet in list_worksheets:
        if wsheet.title == title:
            return wsheet


def create_worksheet(title):
    sheet = _get_sheet()

    succes = _find_sheet_by_title(title)

    if succes is not None:
        raise WorksheetExists(f'worksheet {title}')

    sheet.add_worksheet(title=title, rows=100, cols=20)
    return True


def delete_worksheet(title):
    sheet = _get_sheet()
    wsheet = _find_sheet_by_title(title)
    if wsheet is None:
        return False

    sheet.del_worksheet(wsheet)
    return True


def append_data(worksheet_name, data):
    sheet = _find_sheet_by_title(worksheet_name)
    if sheet is None:
        return False
    records = sheet.get_all_values()
    if records != [[]]:
        sheet.update(records + data)
    else:
        sheet.update(data)
    return True


def pop_data(worksheet_name):
    sheet = _find_sheet_by_title(worksheet_name)
    if sheet is None:
        return False
    records = sheet.get_all_values()
    records[-1] = [""]
    sheet.update(records)
    return True


def list_worksheets_titles():
    sheet = _get_sheet()
    return [i.title for i in sheet.worksheets()]


def _cleanup_test():
    sheet = _get_sheet()
    for i in sheet.worksheets()[1:]:
        if 'test' in i.title:
            delete_worksheet(i.title)


def main_test_api():

    _cleanup_test()
    import faker
    f = faker.Faker()
    sheet = _get_sheet()

    title = 'test ' + f.name()

    create_worksheet(title)
    res = sheet.worksheets()
    assert title in [i.title for i in sheet.worksheets()]

    data = [['a']] * 3
    res = append_data(title, data)
    assert res

    s = _find_sheet_by_title(title)
    v = s.get_values()

    assert v == data, (len(v), v)

    pop_data(title)
    pop_data(title)

    s = _find_sheet_by_title(title)
    v = s.get_values()

    assert v == [['a']], v

    # success = delete_worksheet(title)
    # assert success
    # assert title not in [i.title for i in sheet.worksheets()]


if __name__ == "__main__":
    main_test_api()
    print("success")
