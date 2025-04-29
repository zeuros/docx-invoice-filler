import sys
import json
import locale
import calendar
from datetime import datetime, timedelta
from docx import Document
from docxtpl import DocxTemplate
import jinja2

if __name__ == "__main__":

    print (sys.argv[1])
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: pipenv run python fillInvoice.py <docxTemplateAndJsonName>")
        sys.exit(1)

    # Get the parameter from the command line arguments
    docxAndTemplateName = sys.argv[1]

    # Load my data
    my_data = {}
    with open(f'templates/{docxAndTemplateName}.json', 'r') as file:
        my_data = json.load(file)

    tva = my_data["tva"]
    invoice_number = my_data["invoice_number"]
    billing_month = my_data["invoice_month"] # 3=march
    unit_price_ht =  my_data["unit_price_ht"]
    quantity = my_data["quantity"]
    my_name = my_data["my_name"]
    client_name = my_data["client_name"]
    file_prefix = my_data["file_prefix"]


    # Compute a few variables
    locale.setlocale(locale.LC_TIME, my_data["locale"])
    invoice_month = calendar.month_name[billing_month]
    amount_ht = int(100 * (float(quantity) * float(unit_price_ht)))
    today = datetime.today()
    this_month_end_date = (datetime.today().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    total_ttc = amount_ht * (1 + (tva / 100))
    tva_amount = total_ttc - amount_ht


    # Template variables
    replacements = {}
    replacements["INVOICE_NUMBER"] = invoice_number
    replacements["VAT"] = f"{tva_amount/100:.2f}"
    replacements["TTC"] = f"{total_ttc/100:.2f}"
    replacements["BILLING_MONTH_AND_YEAR"] = datetime.today().replace(month=billing_month).strftime("%B %Y")
    replacements["MONTH_END_DATE"] = this_month_end_date.strftime("%d %B %Y")
    replacements["TODAY_DATE"] = today.strftime("%A %d %B %Y")
    replacements["HT"] = f"{amount_ht / 100:.2f}"
    replacements["QTY"] = f"{quantity}"
    replacements["UNIT_PRICE_HT"] = f"{unit_price_ht:.2f}"

    # Generate the output filename
    output_path = f"./{file_prefix}{invoice_number}_{invoice_month}-{today.strftime("%Y")}_{my_name}_{client_name}.docx"

    # Load the document
    doc = DocxTemplate(f'templates/{docxAndTemplateName}.docx')

    # Replace text in the document
    doc.render(replacements, jinja2.Environment(autoescape=True))

    # Save the new document
    doc.save(output_path)
    print(f"Document saved as {output_path}")