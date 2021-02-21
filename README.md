# IRS Webscraper

> A simple webscraping tool the searches the IRS's Previous Products Page.
> The programs returns the product number, title, and minimum / maximum years the form was created and stores the data in JSON / downloads the proper PDF's for said form in a sub directory.
> 

## Author:
> This program was written by Luke Brazil. This is a solution for the technical assessment given to me by Pinwheel. I had a lot of fun doing this project.
## Installation:

> Download attached zip file to your hard drive.

## Libraries Used:
> Python Version: 3.9.1

BeautifulSoup 4.9.2
```
pip3 install beautifulsoup4
```
Requests
```
pip3 install requests
```
Json
```
pip3 install json
```

## Usage:
After installation of required libraries and you are using python 3.9.1:
```
python3 main.py
```
You will then be asked by the terminal to enter a number.
```
1 Form 1040
2 Form W-2
3 Form 1095C
4 Form 1098
5 Form W-9
6 Form W-4
7 Form W-4P
8 Form 8962
9 Form 941
Please choose a form by its number: 1
Choose another form? Type yes if so, type anything else to get forms: 
```
Enter a number between 1 - 9 depending on which form you want to select. To add another form type in yes.

If you want the form to start scraping based off the forms you chose, enter anything but yes.

You will then be asked to choose a range of years that you want to download the matching PDF for.

```
Form 1040 PDF Download Starting Year: Please enter a year between 1864 - 2020 to retrieve: 2013
Form 1040 PDF Download Ending Year: Please enter a year between 2013 - 2020 to retrieve: 2015
```

In this example I chose 2013 - 2015.

Once the program is completed the data for product_number, min_year, and max_year will be stored in the directories 'data.json' file.

```
{
	"forms": [{
		"form_number": "Form 1040",
		"form_title": "U.S. Individual Income Tax Return",
		"min_year": 1864,
		"max-year": 2020
	}, {
		"form_number": "Form W-2",
		"form_title": "Wage and Tax Statement (Info Copy Only)",
		"min_year": 1954,
		"max-year": 2021
	}]
}
```

The PDF's in the selected range will be downloaded in the sub directory 'form_pdfs'.

## Code Snippets:

Prompt user to choose forms for scraping:

```
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
```

Prompt user for range and use those values to loop through:

```
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
```

## Challenges:
* Taking the form name from the 'selected_forms' array and putting it into the url.
    * Solution: taking the form name and using the .split(" ") method. It turns the string into two items in a array. I then put the two items at the proper place in the url.
    ```
        for form in selected_forms:

        # Turn the form name into an array to insert into url

        url_formatted_form_name = form.split(" ")
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={url_formatted_form_name[0]}+{url_formatted_form_name[1]}&isDescending=false"

    ```
  
* Using the form name to see if it matches the form in the IRS's HTML. Once I see the form name is the same as the form name used in their anchor tag, I need to loop through the row.
    * Solution: Use the beautiful soup library to target certain tags and store the information.
    ```
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
    ```
* Take the data product_number, title, and min / max years and store those values in a dictionary to be written into JSON later.
    * Solution: Appended the data inside a 'Forms' array inside my dictionary. Then take that data and write it into a JSON file.
    ```
    # Storing data in data Dictionary

        data['forms'].append({
            "form_number": form_number,
            "form_title": form_title,
            "min_year": min_year,
            "max-year": max_year
        })
    ```
  Storing the Data
    ```
            with open('data.json', 'w') as file:
            json.dump(data, file)
    ```

## Final Thoughts:
It was extremely refreshing to do such a unique and fun technical assessment. Learning more about Beautiful Soup has given me a lot of ideas for some new fun projects. I would like to thank the team at Pinwheel for considering me and I hope this project finds you well :D! 
