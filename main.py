import pymysql.cursors
from creds import *  # Ensure this contains your database credentials
from pets import Pets  # Import the Pets class from the separate file

# Connect to the database
try:
    myConnection = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        db=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Database connection established.")  # Debugging line
except Exception as e:
    print(f"An error has occurred. Exiting: {e}")
    exit()

# Create a list to hold Pets instances
pets_list = []

# Fetch pet data and create Pets instances
try:
    with myConnection.cursor() as cursor:
        # Modify the SQL query to perform a LEFT JOIN to include pets without matching owners
        sqlSelect = """
            SELECT pets.name, pets.animal_type_id, pets.age, owners.name as owner_name
            FROM pets
            LEFT JOIN owners ON pets.owner_id = owners.id;
        """
        cursor.execute(sqlSelect)

        # Fetch all results at once
        rows = cursor.fetchall()

        if not rows:
            print("No pets found in the database.")  # Informative message
        else:
            pets_list.clear()  # Clear the list to avoid duplicates
            # Create Pets instances
            for row in rows:
                owner_name = row['owner_name'] if row['owner_name'] else "Unknown Owner"  # Handle NULL owner
                pet = Pets(row['name'], row['animal_type_id'], owner_name, row['age'])
                pets_list.append(pet)  # Add to the pets list

except Exception as e:
    print(f"An error occurred while fetching pet data: {e}")

# Function to display pet choices
def display_pet_choices():
    print("\nChoose a pet by serial number or enter 'Q' to quit:")
    for index, pet in enumerate(pets_list, start=1):
        print(f"[{index}] {pet.name}")

# Main loop to ask the user for a pet choice
while True:
    # Display pet choices
    display_pet_choices()

    user_input = input("Enter your choice: ").strip()  # Get user input

    if user_input.lower() == 'q':
        print("Exiting the program. Goodbye!")
        break  # Exit the loop and program

    try:
        choice = int(user_input) - 1  # Convert to index

        if 0 <= choice < len(pets_list):
            chosen_pet = pets_list[choice]
            # Print the chosen pet's info in a concise format
            print(f"\nYou have chosen {chosen_pet.name}, the {chosen_pet.animal_type}. {chosen_pet.name} is {chosen_pet.age} years old. {chosen_pet.name}'s owner is {chosen_pet.owner}.")
            input("Press [ENTER] to continue.")  # Wait for user input
        else:
            print("Invalid choice. Please select a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number corresponding to your choice or 'Q' to quit.")

# Close the database connection
myConnection.close()  # Close connection after data is fetched
print("Database connection closed.")
