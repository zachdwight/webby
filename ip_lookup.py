import ipaddress
import requests
import csv

def get_ip_location(ip_address):
    """
    Retrieves the location and organization name of an IP address using an IP geolocation API.

    Args:
        ip_address (str): The IP address to look up.

    Returns:
        tuple: A tuple containing the city, country, and organization name, or None if an error occurs.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["status"] == "success":
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")
            org = data.get("org", "Unknown")
            orgname = data.get("asname","Unknown")
            return city, country, org, orgname
        else:
            print(f"IP geolocation API error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during IP geolocation lookup: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing geolocation response: {e}")
        return None

def parse_log_file(log_file_path, output_csv_path):
    """
    Parses a log file, extracts IP addresses, retrieves location and organization info, and saves to a CSV file.

    Args:
        log_file_path (str): The path to the log file.
        output_csv_path (str): The path to the output CSV file.
    """
    unique_ips = set()
    try:
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                parts = line.split(" ")
                if len(parts) > 0:
                    ip_address = parts[0]
                    try:
                        ipaddress.ip_address(ip_address)  # Validate is real IP
                        unique_ips.add(ip_address)
                    except ValueError:
                        print(f"Invalid IP address found: {ip_address}")

        with open(output_csv_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["IP Address", "City", "Country", "Organization", "ASName"])  # Write header

            for ip in unique_ips:
                location = get_ip_location(ip)
                if location:
                    city, country, org = location
                    csv_writer.writerow([ip, city, country, org, orgname])
                else:
                    csv_writer.writerow([ip, "Unknown", "Unknown", "Unknown", "Unknown"])

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
log_file_path = "access.log"  # Replace with your log file path
output_csv_path = "ip_locations.csv"  # Replace with your desired output CSV file path
parse_log_file(log_file_path, output_csv_path)
