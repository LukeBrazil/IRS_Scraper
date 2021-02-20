from bs4 import BeautifulSoup
import requests
import json

forms = []
data = {"Form": []}
year_data = []
min_max_years = []
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




url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value=form+w-2&isDescending=false'

response = requests.get(url)
html_text = response.content

soup = BeautifulSoup(html_text, 'lxml')

data_table = soup.find_all('tr', {'class': ['even', 'odd']})

for row in data_table:
    form_product_number = row.td.a.text
    if form_product_number == 'Form W-2':
        year_row = row.find('td', class_='EndCellSpacer').text.strip()
        year_integer = int(year_row)
        form_pdf_url = row.td.a['href']
        title = row.find('td', class_='MiddleCellSpacer').text.strip()
        form_title = title
        form_number = form_product_number
        add_years(row)
        pdf_file = requests.get(form_pdf_url)
        if year_integer >= 2018:
            with open(f"form_pdfs/{form_product_number} - {year_integer}.pdf", 'wb') as file:
                file.write(pdf_file.content)


min_max_years.append([year_data[0], year_data[-1]])
min_year = min_max_years[0][0]
max_year = min_max_years[0][1]
data["Form"].append({
    "form_number": form_number,
    "form_title": form_title,
    "min_year": min_year,
    "max-year": max_year
})

with open('data.json', 'w') as file:
    json.dump(data, file)

print(data)