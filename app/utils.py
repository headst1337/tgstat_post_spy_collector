from io import BytesIO
from openpyxl import Workbook


def generate_excel_report(posts):
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'ID'
    sheet['B1'] = 'Post Link'
    sheet['C1'] = 'Group Link'
    sheet['D1'] = 'Body'
    sheet['E1'] = 'Payment Data'
    sheet['F1'] = 'Timestamp'
    for row, post in enumerate(posts, start=2):
        sheet.cell(row=row, column=1, value=post.id)
        sheet.cell(row=row, column=2, value=post.post_link)
        sheet.cell(row=row, column=3, value=post.group_link)
        sheet.cell(row=row, column=4, value=post.body)
        sheet.cell(row=row, column=5, value=post.payment_data)
        sheet.cell(row=row, column=6, value=post.timestamp)
    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output
