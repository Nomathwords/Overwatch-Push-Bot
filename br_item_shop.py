import urllib.request, json, requests
from requests.auth import HTTPBasicAuth

# Main function to construct the shop output
def construct_shop_photo():

    returned_message = ""

    # Get the shop in JSON format
    json_shop = get_jsonified_shop()

    # If we get nothing, gracefully return with an error message
    if(json_shop == None):
        return "Error fetching shop. Try again later."
    
    # Check if the request was successful
    if json_shop.status_code == 200:
        # Open the file and write the JSON content
        filename = 'output.txt'
        with open(filename, 'w') as outfile:
            outfile.write(json_shop.text)
        print("Items retrieved")
    else:
        return f"Could not retrieve the shop at this time. Error: {json_shop.status_code}"
    
    shop_data = json_shop.json()
    for i in range (0, len(shop_data['shop'])):
        returned_message = returned_message + shop_data['shop'][i]['displayName'] + '\n'

    returned_message.strip()
    return(returned_message)

def get_jsonified_shop():
    try:
        url = 'https://fortniteapi.io/v2/shop?includeRenderData=false&includeHiddenTabs=false'
        headers = {
            'Accept': 'application/json', 
            'Authorization': ''
        }
        
        json_shop = requests.get(url, headers=headers)
        return json_shop
    
    except requests.exceptions.RequestException as e:
        print("Error fetching JSON data:", e)
        return None
