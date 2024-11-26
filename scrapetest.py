from bs4 import BeautifulSoup
import os
import requests


url = "https://en.wikipedia.org/wiki/List_of_animal_names"


def write_to_file(data, filename):
    with open(filename, "w", newline="") as file:
        file.write(str(data))


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
This function receives a list of collateral adjectives and returns a set of unique adjectives.
"""


def parse_collective_adjectives(collateral_adj_split):
    adj_joined_list = []
    for lst in collateral_adj_split:
        adj_joined_list.extend(lst)

    for j in range(
        len(adj_joined_list)
    ):  # Iterate over every collateral adjective in the list, removing suffix of [83], which is citation. This is a quick fix for preventing duplicates.
        try:
            i = adj_joined_list[j].index("[")
            adj_joined_list[j] = adj_joined_list[j][:i]
        except (
            ValueError
        ) as ve:  # If the index is not found, it means the adjective does not contain "[", and we don't care, just continue
            continue

    adj_joined_set = set(adj_joined_list)  # Convert list to a set to remove duplicates
    adj_joined_set.remove("")  # Get rid of the "" key because it spams the results

    return adj_joined_set


"""
This function receives the table data and returns a list of lists
"""


def get_data_from_table(tableData):

    delimiter = "###"  # Add a delimiter to separate collateral adjectives
    for row in tableData:
        for space in row.findAll("br"):
            space.replaceWith(
                delimiter
            )  # Replace <br> tags with delimiter for easier parsing, not necessarily the best way to go, but easy and gets the job done
    tableData = [
        [td.text for td in row.find_all("td")] for row in tableData
    ]  # Get data from table in lists format

    return tableData


"""
This function is used for getting animals and their collateral adjectives, 
returns a list of tuples (animal name, collateral adjective), 
along with the collateral adjectives, and the animal names, for comfortable use
"""


def get_animals_and_collateral_adjectives():

    animal_names = [
        row[0] for row in parsedTable if len(row) > 0
    ]  # Get animal names, filtering out empty entries
    collateral_adj = [
        row[5] for row in parsedTable if len(row) > 0
    ]  # Get collateral adjectives, filtering out empty entries

    animal_names_with_collateral_adj = (
        [  # Create tuples of (animal name, collateral adjective)
            (name, col) for name, col in zip(animal_names, collateral_adj)
        ]
    )
    return animal_names_with_collateral_adj, collateral_adj, animal_names


tableData = get_html_content(
    url
)  # Use bs4 to parse the HTML content and return a table

parsedTable = get_data_from_table(tableData)  # Extracting the data from the table

animal_names_with_collateral_adj, collateral_adj, animal_names = (
    get_animals_and_collateral_adjectives()
)  # Get the animals and their collateral adjectives

# print("THESE ARE ANIMAL NAMES", animal_names)

collateral_adj_split = [
    adj.split("###") for adj in collateral_adj
]  # This is the first step in parsing the collateral adjectives

col_adj_set = parse_collective_adjectives(
    collateral_adj_split
)  # Send the collective adjectives for parsing, returning only real and unique adjectives in a set ("remove -, '', etc.")

adjectives_with_animals = (
    dict()
)  # Initialize the result dictionary which will map adjectives to their proper animals

for (
    key
) in col_adj_set:  # Iterate over every collective adjective that we have in the set
    for (
        animal
    ) in (
        animal_names_with_collateral_adj
    ):  # Iterate over each animal in the (animal, adjectives) tuple
        adjectives_list = animal[1].split(
            "###"
        )  # Break down the adjectives to avoid duplication and incorrectly adding substrings instead of the exact adjectives
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


"""
This function implements some basic tests for the result.
"""


def test_get_animals_and_collateral_adjectives():

    assert len(animal_names) == 231, "The number of animals is not as expected"

    assert (
        len(adjectives_with_animals["canine"]) == 2
    ), "The 'canine' adjective is not mapped to the correct animals"
    assert (
        len(adjectives_with_animals["cervine"]) == 3
    ), "The 'cervine' adjective is not mapped to the correct animals"
    assert (
        len(adjectives_with_animals["musteline"]) == 6
    ), "The 'musteline' adjective is not mapped to the correct animals"


test_get_animals_and_collateral_adjectives()  # Run the test function

write_to_file(
    adjectives_with_animals, "ANIMAL_TEST.txt"
)  # Outputting the result dictionary


# print("All tests passed!")  # If all tests pass, print this message
