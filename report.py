import pandas as pd
from openpyxl.styles import Alignment


def export_results(matches, output_file):
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        matches.to_excel(writer, index=False)

        worksheet = writer.sheets["Sheet1"]

        worksheet.column_dimensions["A"].width = 12
        worksheet.column_dimensions["B"].width = 24
        worksheet.column_dimensions["C"].width = 12
        worksheet.column_dimensions["D"].width = 24

        for column in ["E", "F", "G", "H", "I", "J", "K", "L"]:
            worksheet.column_dimensions[column].width = 18

        worksheet.column_dimensions["M"].width = 45
        worksheet.column_dimensions["N"].width = 35

        for cell in worksheet["M"]:
            cell.alignment = Alignment(wrap_text=True)

        for cell in worksheet["N"]:
            cell.alignment = Alignment(wrap_text=True)

        worksheet.freeze_panes = "A2"