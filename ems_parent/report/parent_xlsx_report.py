from odoo import models

class ParentXlsxReport(models.AbstractModel):
    _name = 'report.ems_parent.parent_elsx_report'  # Keep the hyphen
    _inherit = 'report.report_xlsx.abstract'




    def generate_xlsx_report(self, workbook, data, parents):
        # bold_format = workbook.add_format({'bold': True, 'bg_color': '#ADD8E6'})
        border_format = workbook.add_format({'border': 1})
        bold_format = workbook.add_format({'bold': True, 'bg_color': '#ADD8E6', 'align': 'center'})

        # Create a single sheet
        sheet = workbook.add_worksheet()

        # Add a big header for the school parent records with a light blue background
        # sheet.merge_range('A1:C1', 'School Parent Records', bold_format)
        sheet.merge_range('A1:E2', 'School Parent Records', bold_format)

        # Set column widths
        sheet.set_column('A:E', 15)

        # Write headers for parent details
        headers = ['Name', 'Relation', 'Phone', 'Email', 'Address']
        for col_num, header in enumerate(headers):
            sheet.write(2, col_num, header, bold_format)

        # Write parent details
        data_row = 3
        for obj in parents:
            # Write parent information with borders
            sheet.write(data_row, 0, obj.name, border_format)
            sheet.write(data_row, 1, obj.relation, border_format)
            sheet.write(data_row, 2, obj.phone, border_format)
            sheet.write(data_row, 3, obj.email, border_format)
            sheet.write(data_row, 4, obj.address, border_format)
            # You need to replace 'children' with the actual related field in your model
            # sheet.write(data_row, 5, obj.children, border_format)
            data_row += 1

        # Adjust column widths
        for col_num, header in enumerate(headers):
            sheet.set_column(col_num, col_num, len(header) + 2)


    # def generate_xlsx_report(self, workbook, data, parents):
    #     # Add cell formats
    #     bold_format = workbook.add_format({'bold': True})
    #     date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    #     # Create a single sheet
    #     sheet = workbook.add_worksheet()

    #     # Write headers
    #     headers = ['Name', 'Birthdate', 'Gender', 'Email', 'Phone']
    #     for col_num, header in enumerate(headers):
    #         sheet.write(0, col_num, header, bold_format)

    #     # Write data
    #     data_row = 1
    #     for obj in parents:
    #         sheet.write(data_row, 0, obj.name)
    #         sheet.write(data_row, 1, obj.dob, date_format)
    #         sheet.write(data_row, 2, obj.gender)
    #         sheet.write(data_row, 3, obj.email)
    #         sheet.write(data_row, 4, obj.phone)
    #         data_row += 1

    #     # Adjust column widths
    #     for col_num, header in enumerate(headers):
    #         sheet.set_column(col_num, col_num, len(header) + 2)


# this function generates signal sheet for each parent
    # def generate_xlsx_report(self, workbook, data, parents):
    #     for obj in parents:
    #         report_name = obj.name
    #         sheet = workbook.add_worksheet(report_name[:31])

    #         # Add cell formats
    #         bold_format = workbook.add_format({'bold': True})
    #         date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    #         # Write headers
    #         headers = ['Name', 'Birthdate', 'Gender', 'Email', 'Phone']
    #         for col_num, header in enumerate(headers):
    #             sheet.write(0, col_num, header, bold_format)

    #         # Write data
    #         data_row = 1
    #         sheet.write(data_row, 0, obj.name)
    #         sheet.write(data_row, 1, obj.dob, date_format)
    #         sheet.write(data_row, 2, obj.gender)
    #         sheet.write(data_row, 3, obj.email)
    #         sheet.write(data_row, 4, obj.phone)

    #         # Adjust column widths
    #         for col_num, header in enumerate(headers):
    #             sheet.set_column(col_num, col_num, len(header) + 2)


        # def generate_xlsx_report(self, workbook, data, parents):
    #     bold_format = workbook.add_format({'bold': True, 'bg_color': '#ADD8E6', 'align': 'center'})
    #     border_format = workbook.add_format({'border': 1})

    #     # Create a single sheet
    #     sheet = workbook.add_worksheet()

    #     # Add a big header for the school parent records with a light blue background
    #     sheet.merge_range('A1:E3', 'School Parent Records', bold_format)

    #     # Set column widths to None for autofit
    #     sheet.set_column('A:E', None)

    #     # Write headers for parent details
    #     headers = ['Name', 'Relation', 'Phone', 'Email', 'Address']
    #     for col_num, header in enumerate(headers):
    #         sheet.write(3, col_num, header, bold_format)

    #     # Write parent details
    #     data_row = 4
    #     for obj in parents:
    #         # Write parent information with borders
    #         sheet.write(data_row, 0, obj.name, border_format)
    #         sheet.write(data_row, 1, obj.relation, border_format)
    #         sheet.write(data_row, 2, obj.phone, border_format)
    #         sheet.write(data_row, 3, obj.email, border_format)
    #         sheet.write(data_row, 4, obj.address, border_format)
    #         # You need to replace 'children' with the actual related field in your model
    #         # sheet.write(data_row, 5, obj.children, border_format)
    #         data_row += 1

    #     # Autofit column widths based on content
    #     sheet.autofilter(3, 0, data_row, len(headers) - 1)