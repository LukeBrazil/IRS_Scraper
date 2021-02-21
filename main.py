from bs4 import BeautifulSoup
import requests
import json

forms = []
data = {"Forms": []}
form_title = ''
form_number = ''
url = ''

def format_years(array):
    array.sort()


def add_years(row):
    year_row = row.find('td', class_='EndCellSpacer').text.strip()
    year_integer = int(year_row)
    year_data.append(year_integer)
    format_years(year_data)

def ask_for_form():
    form_input = input("""
Welcome to the form generator. You are to enter the IRS Tax forms that you would like to webscrape.
\n
Format: form + number
Example: form 1095c
\n
>>> """)
    form_input = form_input.title()
    formatted_form_input = form_input.split(" ")
    forms.append(formatted_form_input)
    continue_forms = input('Would you like to add another form?')
    if continue_forms == 'y':
      ask_for_form()
    else:
      pass




while True:
    ask_for_form()
    for form in forms:
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={form[0]}+{form[1]}&isDescending=false"
        response = requests.get(url)
        html_text = response.content
        form_name = form[0] + " " + form[1]

        soup = BeautifulSoup(html_text, 'lxml')

        data_table = soup.find_all('tr', {'class': ['even', 'odd']})
        year_data = []
        min_max_years = []
        link_array = []

        for row in data_table:
            form_product_number = row.td.a.text
            if form_product_number == form_name:
                year_row = row.find('td', class_='EndCellSpacer').text.strip()
                year_integer = int(year_row)
                year_data.append(year_integer)
                form_pdf_url = row.td.a['href']
                title = row.find('td', class_='MiddleCellSpacer').text.strip()
                form_title = title
                form_number = form_product_number
                pdf_file = requests.get(form_pdf_url)
                link_array.append([form_number, year_integer, form_pdf_url])
                # start_year = int(input(f'Please enter a year between you would like to start with for {form_number}. '))
                # while start_year != int:
                #     start_year = int(input(f'Please enter a year you would like to start with for {form_number}: '))
                # if year_integer >= start_year:
                #     with open(f"form_pdfs/{form_product_number} - {year_integer}.pdf", 'wb') as file:
                #         file.write(pdf_file.content)
        min_max_years.append([year_data[0], year_data[-1]])
        min_year = min_max_years[0][0]
        max_year = min_max_years[0][1]
        data["Forms"].append({
            "form_number": form_number,
            "form_title": form_title,
            "min_year": min_year,
            "max-year": max_year
        })
        start_year = int(input(f"{form_number}: Please enter a year greater than {max_year}"))
        for item in link_array:
            if item[1] >= start_year:
                pdf_file = requests.get(item[2])
                with open(f"form_pdfs/{item[0]} - {item[1]}.pdf", 'wb') as file:
                    file.write(pdf_file.content)

        with open('data.json', 'w') as file:
            json.dump(data, file)

    break

