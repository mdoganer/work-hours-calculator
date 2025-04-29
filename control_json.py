import json
from utils import get_file_path  # Import the global get_file_path function


def json_open():
    try:
        # Use the global get_file_path function
        file_name = get_file_path()
        if file_name.exists():
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        else:
            return []
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []


def filter_by_badge(data, badge_number):
    # Filter records for the given badge number
    return [record for record in data if record['sicil'] == badge_number]



def main():
    data = json_open()
    badge_number = input("Lütfen sicil numarasını girin: ")  # Ask user for badge number
    filtered_data = filter_by_badge(data, badge_number)
    
    if filtered_data:
        print(f"\nSicil Numarası: {badge_number} için kayıtlar:\n")
        print(filtered_data)
    else:
        print(f"\nSicil Numarası: {badge_number} için kayıt bulunamadı.\n")


if __name__ == "__main__":
    main()