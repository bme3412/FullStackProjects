from openai import OpenAI
import json
import os

# Initialize your OpenAI client with your actual API key
client = OpenAI(api_key='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')

def get_sports_teams_info_and_save(city_names):
    for city in city_names:
        try:
            normalized_city_name = city.replace(' ', '_')
            prompt = f"""
            For the city of {city}, please list out all the professional sports teams, including details about their venues, average estimated ticket prices, the start of the regular season, the start of playoffs, and format this information in JSON structure as shown:
            {{
                "city": "{city}",
                "sports_teams": [
                    {{
                        "team_name": "Example Team",
                        "sport": "Example Sport",
                        "league": "Example League",
                        "average_ticket_price": "Example Price",
                        "season_start": "Example Start Date of Regular Season",
                        "playoffs_start": "Example Start Date of Playoffs",
                        "venue": {{
                            "venue_name": "Example Venue",
                            "details": "Example Details about the Venue",
                            "address": "Example Address",
                            "geographic_coordinates": {{
                                "latitude": 0.0,
                                "longitude": 0.0
                            }}
                        }}
                    }}
                    // Additional teams can be added here
                ]
            }}
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Correctly access the response content
            if response.choices:
                response_data = response.choices[0].message.content
            else:
                response_data = {}

            # Define the directory and file paths based on the city name
            dir_path = f"data/{normalized_city_name}"
            os.makedirs(dir_path, exist_ok=True)

            file_path = os.path.join(dir_path, f"{normalized_city_name}.json")
            with open(file_path, 'w', encoding='utf-8') as file:
                # Assuming the response_data is a JSON string; otherwise, this will need parsing or conversion
                file.write(response_data)

            print(f"Data for {city} saved successfully in {file_path}.")

        except Exception as e:
            print(f"An error occurred for city {city}: {e}")

# Example usage
city_names = [
    'Atlanta',  # Falcons (NFL), Braves (MLB), Hawks (NBA), United (MLS)
    'Baltimore',  # Ravens (NFL), Orioles (MLB)
    'Boston',  # Patriots (NFL), Red Sox (MLB), Celtics (NBA), Bruins (NHL), Revolution (MLS)
    'Chicago',  # Bears (NFL), Cubs & White Sox (MLB), Bulls (NBA), Blackhawks (NHL), Fire (MLS)
    'Cleveland',  # Browns (NFL), Guardians (MLB), Cavaliers (NBA)
    'Dallas',  # Cowboys (NFL), Rangers (MLB), Mavericks (NBA), Stars (NHL), FC Dallas (MLS)
    'Denver',  # Broncos (NFL), Rockies (MLB), Nuggets (NBA), Avalanche (NHL), Rapids (MLS)
    'Detroit',  # Lions (NFL), Tigers (MLB), Pistons (NBA), Red Wings (NHL)
    'Green Bay',  # Packers (NFL)
    'Houston',  # Texans (NFL), Astros (MLB), Rockets (NBA), Dynamo (MLS)
    'Indianapolis',  # Colts (NFL), Pacers (NBA)
    'Kansas City',  # Chiefs (NFL), Royals (MLB), Sporting KC (MLS)
    'Los Angeles',  # Rams & Chargers (NFL), Dodgers & Angels (MLB), Lakers & Clippers (NBA), Kings & Ducks (NHL), Galaxy & LAFC (MLS)
    'Miami',  # Dolphins (NFL), Marlins (MLB), Heat (NBA), Inter Miami CF (MLS)
    'Milwaukee',  # Brewers (MLB), Bucks (NBA)
    'Minneapolis',  # Vikings (NFL), Twins (MLB), Timberwolves (NBA), Wild (NHL)
    'New Orleans',  # Saints (NFL), Pelicans (NBA)
    'New York',  # Giants & Jets (NFL), Yankees & Mets (MLB), Knicks & Nets (NBA), Rangers, Islanders & Devils (NHL), NYCFC & Red Bulls (MLS)
    'Philadelphia',  # Eagles (NFL), Phillies (MLB), 76ers (NBA), Flyers (NHL), Union (MLS)
    'Phoenix',  # Cardinals (NFL), Diamondbacks (MLB), Suns (NBA), Coyotes (NHL)
    'Pittsburgh',  # Steelers (NFL), Pirates (MLB), Penguins (NHL)
    'Portland',  # Trail Blazers (NBA), Timbers (MLS)
    'San Antonio',  # Spurs (NBA)
    'San Diego',  # Padres (MLB)
    'San Francisco',  # 49ers (NFL), Giants (MLB), Golden State Warriors (NBA), Earthquakes (MLS)
    'Seattle',  # Seahawks (NFL), Mariners (MLB), Sounders (MLS), Kraken (NHL)
    'St Louis',  # Cardinals (MLB), Blues (NHL)
    'Tampa Bay',  # Buccaneers (NFL), Rays (MLB), Lightning (NHL)
    'Toronto',  # Raptors (NBA), Blue Jays (MLB), Maple Leafs (NHL), Toronto FC (MLS)
    'Vancouver',  # Canucks (NHL), Whitecaps FC (MLS)
    'Washington',  # Redskins (NFL), Nationals (MLB), Wizards (NBA), Capitals (NHL), D.C. United (MLS)
    'London'  # Various Premier League Teams, etc.
]

get_sports_teams_info_and_save(city_names)
