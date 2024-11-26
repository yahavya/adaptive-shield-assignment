import csv
from bs4 import BeautifulSoup
import requests


url = "https://en.wikipedia.org/wiki/List_of_animal_names"

"""
Function for getting html content from the url, parsing it with bs4 and returning a table.
"""


def get_html_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        doc = response.text
        soup = BeautifulSoup(doc, "html.parser")
        # tables = soup.find_all("tbody")[2]
        # tables = soup.findChildren("tbody")[2]
        table = soup.find_all("tbody")[2].find_all("tr")

    return table


"""
Function for writing data to a specified filename in CSV format.
"""


def write_to_file(data, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        # writer.writerow(["Name", "Origin", "Classification", "Family"])
        writer.writerows(data)


tableData = get_html_content(url)
delimiter = "###"


for row in tableData:
    for space in row.findAll("br"):
        space.replaceWith(delimiter)


tableData = [[td.text for td in row.find_all("td")] for row in tableData]

animal_names = [row[0] for row in tableData if len(row) > 0]  # Get animal names
collateral_adj = [
    row[5] for row in tableData if len(row) > 0
]  # Get collateral adjectives

animal_names_with_collateral_adj = (
    [  # Create tuples of (animal name, collateral adjective)
        (name, col) for name, col in zip(animal_names, collateral_adj)
    ]
)

collateral_adj_split = [adj.split("###") for adj in collateral_adj]


def get_collective_adjectives_set(collateral_adj_split):
    adj_joined_list = []
    for lst in collateral_adj_split:
        adj_joined_list.extend(lst)

    for j in range(len(adj_joined_list)):
        try:
            i = adj_joined_list[j].index("[")
            adj_joined_list[j] = adj_joined_list[j][:i]
            # print("found item", adj_joined_list[j], "with substring")
        except ValueError as ve:
            continue

    adj_joined_set = set(adj_joined_list)
    adj_joined_set.remove("")  # Get rid of the "" key because it spams the results
    return adj_joined_set


def is_exactly(s):

    return False


adj_set = get_collective_adjectives_set(
    collateral_adj_split
)  # Send the collective for parsing, returning only unique and clean adjectives

adjectives_with_animals = (
    dict()
)  # Initialize the result dictionary which will map adjectives to their proper animals

for key in adj_set:  # Iterate over every collective adjective that we have
    for (
        animal
    ) in (
        animal_names_with_collateral_adj
    ):  # Iterate over each animal in the (animal, adjectives) tuple
        adjectives_list = animal[1].split("###")
        if (
            key in adjectives_list
        ):  # Check if the adjective is in one of the animal's adjectives

            if key not in adjectives_with_animals:
                adjectives_with_animals[key] = [
                    animal[0]
                ]  # If the key isn't already in the dictionary, initialize an entry with it
            else:
                adjectives_with_animals[key].append(
                    animal[0]
                )  # Otherwise, add the animal to the proper (key,value) pair.

print(adjectives_with_animals)
