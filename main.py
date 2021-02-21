from bs4 import BeautifulSoup
import requests
import json

# Initial forms for use

forms = ['Form 1040', 'Form W-2', 'Form 1095C', 'Form 1098', 'Form W-9', 'Form W-4', 'Form W-4P', 'Form 8962', 'Form 941']

# Forms selected from input

selected_forms = []

# Dictionary used to store the product number, title, and min / max year for forms.

data = {'forms': []}


# Add forms through input function. Runs at the top of the while loop

def add_forms():
    # enumerate forms for easy selection
    for index, form in enumerate(forms):
        print(index + 1, form)

    # Input to choose form

    chosen_form = int(input('Please choose a form by its number: '))

    # Add chosen form to selected_forms array

    selected_forms.append(forms[chosen_form - 1])

    # Input to continue

    choice = input('Choose another form? Type yes if so, type anything else to get forms: ')
    if choice.lower() == 'yes':
        print(f'Selected Forms: {selected_forms}')
        add_forms()
    else:
        print('')
        print(f'Working on {selected_forms} ....')
        print('')
        pass

# Main while loop

while True:
    add_forms()
    # Loop through forms in selected_forms array

    for form in selected_forms:

        # Turn the form name into an array to insert into url

        url_formatted_form_name = form.split(" ")
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={url_formatted_form_name[0]}+{url_formatted_form_name[1]}&isDescending=false"

        # Using Requests library to retrieve the data

        response = requests.get(url)

        # Storing the data as an object to be iterated on

        html_text = response.content

        # Using the Beautiful Soup library to parse the html

        soup = BeautifulSoup(html_text, 'lxml')

        # Selecting all the <tr>'s that store the data in the table

        data_table = soup.find_all('tr', {'class': ['even', 'odd']})

        # Initiating arrays to store individual form data

        year_data = []  # Stores all the years for each item
        link_array = []  # Stores form number, year, and url for each form

        # Looping through each individual row

        for row in data_table:
            # Stores name of form ex. Form W-2

            form_product_number = row.td.a.text
            if form_product_number == form:
                # Selected the year for the form

                year_row = row.find('td', class_='EndCellSpacer').text.strip()
                year_integer = int(year_row)

                # Add it to the year data array

                year_data.append(year_integer)

                # Store url for PDF

                form_pdf_url = row.td.a['href']

                # Store the description of the form

                title = row.find('td', class_='MiddleCellSpacer').text.strip()

                # Creating the variable to store in JSON

                form_title = title
                form_number = form_product_number

                # Appending data to the link_array

                link_array.append([form_number, year_integer, form_pdf_url])

        # Sort the year_data array ascending

        year_data.sort()

        # Creating min / max year variables from year_data array

        if year_data:
            max_year = year_data[len(year_data) - 1]
            min_year = year_data[0]
        else:
            pass

        # Storing data in data Dictionary

        data['forms'].append({
            "form_number": form_number,
            "form_title": form_title,
            "min_year": min_year,
            "max-year": max_year
        })

        # Asking for user input to create start / end year range. This range will be used to download the proper PDF's

        start_year = int(
            input(f"{form_number} PDF Download Starting Year: Please enter a year between {min_year} - {max_year} to retrieve: "))
        end_year = int(
            input(f"{form_number} PDF Download Ending Year: Please enter a year between {start_year} - {max_year} to retrieve: "))

        # Looping through min / max year range

        for index in range(start_year, end_year + 1):
            # Looping through items in link_array

            for item in link_array:
                # Checking if the year chosen by input equals the year in the item.

                if item[1] == index:
                    # Using the requests library to fetch the PDF Url
                    pdf_file = requests.get(item[2])
                    # Writing the PDF file to a the sub directory '/form_pdfs'
                    # item[0] is the form name / item[1] is the year the form was created.
                    with open(f"form_pdfs/{item[0]} - {item[1]}.pdf", 'wb') as file:
                        file.write(pdf_file.content)

        # Writing product number, title, and min / max years to the 'data.json' file in this directory.

        with open('data.json', 'w') as file:
            json.dump(data, file)
        print('')
        print('Working.....')
        print('')

    # Ending the program
    print("Data sent to JSON file and PDF's have been saved in your subdirectory.")
    break
