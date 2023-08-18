# Imoport requests and BeautifulSoup4 modules
import requests
from bs4 import BeautifulSoup

# A function to determine if a string contains letters (is a word)
def contains_at_least_one_letter(input_string):
    return any(char.isalpha() for char in input_string)

# A function to determine if a string is a link (contains the "[")
def notalink(input_string):
    return not any(char=="[" for char in input_string)

# A function to get the exact name of the animal (gets only the value that comes before "(list)", "Also see", or a link ("["))
def extract_text(input_string):
    list_index = input_string.find("(list)")
    also_see_index = input_string.find("Also see")
    link_index = input_string.find("[")
    idx_dict = [idx for idx in (list_index, also_see_index,link_index) if idx != -1]
    if idx_dict:
        index = min(idx_dict)
        return input_string[:index].strip()
    else:
        return input_string

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_animal_names"

# Send a request to the URL and retrieve the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the <h2> tag with the "Terms_by_species_or_taxon" 
Terms_by_species_or_taxon_header = soup.find(id="Terms_by_species_or_taxon")

# Find the table that comes after the Terms by species or taxon header
table = Terms_by_species_or_taxon_header.find_next("table")

# Find the columns titles in the header row
header_row = table.find('tr')
column_titles = [header.get_text(strip=True) for header in header_row.find_all('th')]

# Find the column numbers for the relevant sections
animal_column_index = column_titles.index('Animal')
collateral_adjective_column_index = column_titles.index('Collateral adjective')
collective_noun_column_index = column_titles.index('Collective noun')

# Iterate through each row in the table
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')

    # Check if a row has more than 3 cells (to ignore the letters' rows)
    if len(columns) >= 3:

        # Gets the values of the relevant cells
        animal_name = columns[animal_column_index].text.strip()
        collateral_adjective = columns[collateral_adjective_column_index].text.strip()
        collective_noun_text = columns[collective_noun_column_index].text.strip()
        animal_name = extract_text(animal_name)

        # Check if an animal has a Collective noun (ignoring "-", "?" or anything that is not a word), and prints the animal name and the Collateral adjective if so
        if not contains_at_least_one_letter(collective_noun_text):
                print(animal_name,"- ",collateral_adjective)
        else:
            # Seperate the Collective nouns and ignoring the links
            collective_noun_text = columns[collective_noun_column_index]
            nouns = "\n".join(text for text in collective_noun_text.stripped_strings)
            for noun in nouns.split('\n'):
                if notalink(noun):
                    # If an animal has Collective nouns, print the animal name with each noun in a seperate line 
                    print(animal_name,"- ",noun)

