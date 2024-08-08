import phonenumbers
from phonenumbers import geocoder, carrier, phonenumberutil, timezone
from geopy.geocoders import Nominatim
import folium
import pyfiglet
from colorama import Fore, Style, init
import requests

# Initialize colorama
init(autoreset=True)

# Generate title and subtitle using pyfiglet
title = pyfiglet.figlet_format("NX Pro", font="block")
subtitle = pyfiglet.figlet_format("Phone Number Details Extractor", font="digital")
titletext = "NX Pro Phone Number Details Extractor"

# Print title, titletext, and subtitle in green
print(Fore.GREEN + title)
print(Fore.GREEN + titletext)
print(Fore.GREEN + subtitle)


print("📞 Welcome to the NX Pro Phone Number Details Extractor by Redx! 📞")
print("Please enter the phone number below:")

phone_number = input("Enter the phone number: ")

try:
    number = phonenumbers.parse(phone_number, None)
    country_code = phonenumbers.region_code_for_number(number)
    location = geocoder.description_for_number(number, "en")
    carrier_name = carrier.name_for_number(number, "en") or "Unknown Carrier"
    
    number_type = phonenumberutil.number_type(number)
    number_type_description = phonenumberutil.PhoneNumberType.MOBILE if number_type == phonenumberutil.PhoneNumberType.MOBILE else "Other"
    
    validity = "Valid" if phonenumbers.is_valid_number(number) else "Invalid"
    formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    country_name = geocoder.country_name_for_number(number, "en")
    is_possible = "Possible" if phonenumbers.is_possible_number(number) else "Not possible"
    
    time_zones = timezone.time_zones_for_number(number)
    time_zones_description = ", ".join(time_zones) if time_zones else "Time zone information not available"
    
    national_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)
    e164_format = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
    
    # Initialize the geolocator
    geolocator = Nominatim(user_agent="phone-number-geocoder")
    latitude, longitude = None, None
    map_url = None
    
    if location and location != "Unknown":
        geo_location = geolocator.geocode(location)
        if geo_location:
            latitude = geo_location.latitude
            longitude = geo_location.longitude
            map_url = f"https://www.google.com/maps/@{latitude},{longitude},15z"

    # Create an interactive map using folium if coordinates are available
    if latitude and longitude:
        map = folium.Map(location=[latitude, longitude], zoom_start=12)
        folium.Marker([latitude, longitude], popup=f"Location: {location}").add_to(map)
        map.save("phone_location_map.html")
        print(f"\n🗺️ Map generated and saved as 'phone_location_map.html'.")

    details = {
        "Country Code": country_code,
        "Country Name": country_name,
        "Location": location,
        "Latitude": latitude,
        "Longitude": longitude,
        "Sim Name": carrier_name,
        "Number Type": number_type_description,
        "Validity": validity,
        "Formatted Number": formatted_number,
        "Is Possible Number": is_possible,
        "Time Zones": time_zones_description,
        "National Number": national_number,
        "E164 Format": e164_format,
        "Map URL": map_url or "Map not available"
    }
    
    print("\n🌐 Phone Number Details 🌐:")
       
    for key, value in details.items():
        print(f"{key}: {value}")

except phonenumbers.phonenumberutil.NumberParseException as e:
    print("❌ Number could not be parsed:", e)

except Exception as e:
    print(f"❌ An error occurred: {e}")

