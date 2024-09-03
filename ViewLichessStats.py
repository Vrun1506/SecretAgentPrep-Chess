import json
import berserk
import matplotlib.pyplot as plt
from datetime import datetime

def return_lichess_data():
    API_TOKEN = "lip_dWBg5ZzgY80s4F3rbE9y"  # This is the API token that is linked to my end user's account. I was able to obtain this through detailing a series of instructions on an email. 
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session) # There is no way of me being able to access my end user's details other than through using the Python client for the Lichess API. 
    
    try:
        data = client.account.get()  # This function gets all of the data that is associated with the account that the API token is linked to. 
    except berserk.BerserkError as e: # To deal with any errors that may arise. 
        print(f"Error retrieving lichess data: {e}")
        data = None

    if data:
        # Save data to a JSON file
        with open('player_data.json', 'w') as file:   # The data is arriving in a dictionary format so the data is being stored in a JSON file before being manipulated.
            json.dump(data, file, default=str)  # Using default=str to handle datetime objects

def fetch_games(user_id, variant):
    # This function returns a list of the last 10 games of a particular variant in PGN format
    API_TOKEN = "lip_dWBg5ZzgY80s4F3rbE9y"
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    
    try:
        # Fetch the last 10 games played by the user in PGN format
        games_pgn = client.games.export_by_player(user_id, rated=True, perf_type=variant, clocks=False, max=10, as_pgn=True)
        return games_pgn
    except berserk.BerserkError as e:
        print(f"Error fetching games: {e}")
        return None

def display_pgn(games_pgn):
    # Print PGN for each game
    for game_pgn in games_pgn:
        print(game_pgn)
        print("\n\n")


def draw_ratings_graphs(variants_data):
    # Plotting the line graph for all variants
    plt.figure(figsize=(10, 6))
    for variant, (dates, ratings) in variants_data.items():   #The key
        plt.plot(dates, ratings, marker='o', label=f'{variant.capitalize()} Ratings')

    plt.xlabel('Date')
    plt.ylabel('Rating')
    plt.title("VishnuVadlamani's lichess ratings")
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('all_variants_line_graph.png')  # Save the graph as an image
    plt.gcf().canvas.manager.set_window_title("VishnuVadlamani's lichess ratings")
    plt.show()

    # Empty the "player_data.json" file
    with open('player_data.json', 'w') as empty_file:  # The json file is emptied so there is no confusion with the data the next instance that the code is executed (i.e. the next time that the user enters 2).
        empty_file.write("")

def get_choice():
    # This function gets the choice from the user.
    while True:
        try:
            c = input("--->").lower()  # Get the user choice of what they want to do. 
            if c == "q" or 1 <= int(c) <= 2:
                return c  # A valid input has been provided so it is returned.
            else:
                raise ValueError("Invalid choice. Please enter 1 or 2 or enter Q to quit.")  # rogue input
        except ValueError:
            print("Rogue input detected. Please enter a valid choice.")


def print_choices():
    # This function output to the user the available choices.
    print("1-View PGN of the last 10 games played")
    print("2-View a graph of lichess ratings over time")
    print("Q - Quit the program")


def print_choices():
    # This function output to the user the available choices.
    print("1-View PGN of the last 10 games played")
    print("2-View a graph of lichess ratings over time")
    print("Q - Quit the program")

def get_variant():
    # This function asks the user to select a variant that they would like to see the last 10 games of.
    valid_variant = False
    while not valid_variant:
        variant = input("Select a variant (Bullet, Blitz, Rapid):").lower() 

        if variant not in ["bullet", "blitz", "rapid"] and variant != "": # My end user  has only played four classical games to date which means that it isn't possible to fetch the game data for the last 10 games. Hence, it hasn't been included in the variant list.
            print("Please select a valid variant or press enter to exit")
        else:
            valid_variant = True
            return variant # When a valid variant is selected, the variant will be returned

def get_rating_data():
    # From the data stored in the json file after the data has been fetched from the API, the data is manipulated to fetch the ratings.
    # Each rating is then stored with the date that the rating is fetched in a corresponding text file based off the variant name 

    # Load data from the JSON file
    with open('player_data.json', 'r') as file:
        data = json.load(file)

    # Extracting details
    perfs = data['perfs']

    # Dictionary to store dates and ratings for each variant
    variants_data = {}

    # Extract ratings for each game variant
    for variant in ['bullet', 'blitz', 'rapid', 'classical']:
        rating = perfs.get(variant, {}).get('rating', None)

        if rating is not None:
            # Save rating to the text file
            file_path = f'{variant}_ratings.txt'
            current_entry = f"{datetime.now().strftime('%d/%m/%Y')}\n{rating}\n"

            # Open the file in append mode and create it if it doesn't exist
            with open(file_path, 'a+') as rating_file:
                # Move the cursor to the beginning of the file to read existing entries
                rating_file.seek(0)
                existing_entries = rating_file.readlines()

                if current_entry not in existing_entries:
                    rating_file.write(current_entry)

            # Append dates and ratings to the dictionary
            dates, ratings = [], []
            with open(file_path, 'r') as variant_file:
                lines = variant_file.readlines()
                for i in range(0, len(lines), 2):
                    date_str, rating_str = lines[i].strip(), lines[i+1].strip()

                    # Check if date_str is not an empty string before converting
                    if date_str:
                        dates.append(datetime.strptime(date_str, "%d/%m/%Y"))
                        ratings.append(int(rating_str))

            variants_data[variant] = (dates, ratings)

    return variants_data


def main():
    # The main function. 
    run = True 
    while run: #this will run indefinitely until the user has entered 'q' in the input field.
        print_choices()
        user_choice = get_choice()

        # user choice handling
        if user_choice == "1":
            variant = get_variant()
            user_id = "VishnuVadlamani" # my end user's account username
            games_pgn = fetch_games(user_id, variant)

            if games_pgn:
                display_pgn(games_pgn)

        elif user_choice == "2":
            return_lichess_data()   # This function retrieves the Lichess data and then stores in the player_data.json file. 
            rating_data = get_rating_data()  # This splits the data by rating into different text files. 
            draw_ratings_graphs(rating_data) # This graphically represents the rating data that is present in the text files. 

        elif user_choice.lower() == 'q':  # If the user wants to quit
            run = False
            exit()

if __name__ == "__main__":
    main()