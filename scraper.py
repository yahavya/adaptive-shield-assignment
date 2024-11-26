from bs4 import BeautifulSoup
import requests
import threading
import time


url = "https://en.wikipedia.org/wiki/List_of_animal_names"

"""
This function makes use of the download_images function, with 4 threads running simaltaneously, in order to ensure images are downloaded quickly.
"""


def download_images_with_threading(cleaned_animal_names):
    print("Starting to scrape images from Wikipedia")
    t1 = threading.Thread(
        target=download_images,
        args=[cleaned_animal_names[: len(cleaned_animal_names) // 4]],
    )
    t2 = threading.Thread(
        target=download_images,
        args=[
            cleaned_animal_names[
                len(cleaned_animal_names) // 4 : 2 * len(cleaned_animal_names) // 4
            ]
        ],
    )
    t3 = threading.Thread(
        target=download_images,
        args=[
            cleaned_animal_names[
                2
                * len(cleaned_animal_names)
                // 4 : (3 * len(cleaned_animal_names) // 4)
            ]
        ],
    )
    t4 = threading.Thread(
        target=download_images,
        args=[cleaned_animal_names[(3 * len(cleaned_animal_names) // 4) :]],
    )

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()


"""
This function cleans the animal names for easier use in the download_images function
"""


def clean_animal_names(animal_names):
    for j in range(
        len(animal_names)
    ):  # Iterate over every collateral adjective in the list, removing suffix of [83], which is citation. This is a quick fix for preventing duplicates.
        try:
            animal_names[j] = animal_names[j].replace("(list)", "")
            animal_names[j] = animal_names[j].replace("###Also see", "")
            animal_names[j] = animal_names[j].replace("###See", "")
            animal_names[j] = animal_names[j].replace("See", "")
            i = animal_names[j].index("[")
            animal_names[j] = animal_names[j][:i]
        except (
            ValueError
        ) as ve:  # If the index is not found, it means the adjective does not contain "[", and we don't care, just continue
            continue
    return animal_names


"""
This function receives a list of animal names and downloads images for each animal based on the wikipedia page.
"""


def download_images(cleaned_animal_names):
    error_count = 0
    for name in cleaned_animal_names:
        try:

            response = requests.get(f"https://en.wikipedia.org/wiki/{name}")

            # print("request to " + f"https://en.wikipedia.org/wiki/{name} suceeded")

            if response.status_code == 200:
                doc = response.text
                soup = BeautifulSoup(doc, "html.parser")
                img_tag = (
                    soup.find("tbody")
                    .find("img", {"class": "mw-file-element"})
                    .get("src")
                )

                # print("img tag found", img_tag)

                if img_tag:
                    img_url = "https:" + img_tag
                    img_name = name.replace(" ", "_") + ".jpg"
                    img_response = requests.get(img_url)

                if img_response.status_code == 200:
                    with open(
                        f"adaptive-shield-assignment/tmp/{img_name}", "wb"
                    ) as file:
                        file.write(img_response.content)
                    # print("saved image successfully")
        except:
            print(
                f"Error in getting image for {name}, investigate URL at: "
                f"https://en.wikipedia.org/wiki/{name}"
            )
            error_count += 1
            continue
    print(f"Error in total of {error_count} images")


"""
This function takes the expected result data (dictionary of collateral adjectives each mapped to a list of animal names)
and writes it to a file.
"""


def write_to_file(data, filename):
    with open(filename, "w", newline="") as file:
        file.write(str(data))


"""
This functiion is for getting html content from the url, parsing it with bs4 and returning a table.
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
This function receives a list of collateral adjectives and returns a set of unique adjectives, 
that will be used for looking up which collateral adjectives appear on which animals.
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
This function receives the table data and returns the table as a list of lists.
"""


def get_data_from_table(table_data):

    delimiter = "###"  # Add a delimiter to separate collateral adjectives
    for row in table_data:
        for space in row.findAll("br"):
            space.replaceWith(
                delimiter
            )  # Replace <br> tags with delimiter for easier parsing, not necessarily the best way to go, but easy and gets the job done
    table_data = [
        [td.text for td in row.find_all("td")] for row in table_data
    ]  # Get data from table in lists format

    return table_data


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


### --------------------------------------------------------------------------------------------------------------------------------------- ###

url = "https://en.wikipedia.org/wiki/List_of_animal_names"

table_data = get_html_content(
    url
)  # Use bs4 to parse the HTML content and return a table

parsedTable = get_data_from_table(table_data)  # Extracting the data from the table

animal_names_with_collateral_adj, collateral_adj, animal_names = (
    get_animals_and_collateral_adjectives()
)  # Get the animals and their collateral adjectives

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
    adjectives_with_animals, "RESULT.txt"
)  # Writing the result dictionary to RESULT.txt

cleaned_animal_names = clean_animal_names(
    animal_names
)  # Clean the animal names of suffixes such as ###, [citation], etc.

download_images_with_threading(cleaned_animal_names)

print("Done downloading images!")

# print("All tests passed!")  # If all tests pass, print this message
