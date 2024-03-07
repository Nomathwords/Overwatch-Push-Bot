import urllib.request, json 

# Main function to construct the shop output
def construct_shop_photo():

    returned_message = ""

    # Get the shop in JSON format
    json_shop = get_jsonified_shop()

    # If we get nothing, gracefully return with an error message
    if(json_shop == None):
        return "Error fetching shop. Try again later."

    # If we do get something but the status is 400, also return with an error message
    if(json_shop['status'] == 400):
        return "Could not retrieve the shop at this time. Error: 400 Bad Request"
    
    #
    featured_items = json_shop['data']['featured']['entries']

    for item in featured_items:

        # Bundles are slightly different, and we mainly just want the name and photo of the whole bundle
        if(item['bundle'] is not None):
            print(item['bundle']['name'])
            returned_message = returned_message + item['bundle']['name'] + '\n'
        
        # Get everything else
        else:
            print(item['items'][0]['name'])
            returned_message = returned_message + item['items'][0]['name'] + '\n'
        
    return returned_message

def get_jsonified_shop():
    try:
        with urllib.request.urlopen("https://fortnite-api.com/v2/shop/br/combined") as url:
            json_shop = json.load(url)
        return json_shop
    
    except urllib.error.URLError as e:
        print("Error fetching JSON data:", e)
        return None
