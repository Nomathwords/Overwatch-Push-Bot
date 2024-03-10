import urllib.request, json, requests, shutil, os, asyncio, aiohttp, aiofiles, subprocess
from requests.auth import HTTPBasicAuth
from pathlib import Path
from PIL import Image

# Main function to construct the shop output
async def get_fortnite_shop():

    image_directory_path = "./shop_images"
    image_file_path = "/result.png"
    returned_message = "Hello"

    # Get the shop in JSON format
    json_shop = await get_jsonified_shop()

    # If we get nothing, gracefully return with an error message
    if(json_shop == None):
        return "Error fetching shop. Try again later."
    
    # Check if the request was successful
    if json_shop != None:
        # Open the file and write the JSON content
        filename = 'output.txt'
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(json_shop))
        print("Items retrieved")
    else:
        return "Could not retrieve the shop at this time."
    
    # Fetch the shop images
    await fetch_item_images(json_shop, image_directory_path)

    # Create one large image to send back to Discord
    await create_shop_image(image_directory_path)

    # Make sure the final image exists before returning it
    if os.path.isfile(image_directory_path + image_file_path) == True:
        return(image_directory_path + image_file_path)

    else:
        return("Image failed to generate. Try again later.")

# Function that hits the Fortnite API and gets the shop in JSON form. Requires a valid API key.
async def get_jsonified_shop():
    
    try:
        url = 'https://fortniteapi.io/v2/shop?includeRenderData=false&includeHiddenTabs=false'
        headers = {
            'Accept': 'application/json', 
            'Authorization': ''
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                json_shop = await response.json()
                return json_shop
    
    except aiohttp.ClientError as e:
        print("Error fetching JSON data:", e)
        return None


async def fetch_item_images(json_shop, image_path):

    image_url = ""
    image = None
    display_assets_length = 0

    # Create folder if it does not exist
    if not Path(image_path).is_dir():
        Path(image_path).mkdir()

    # Remove contents from folder if not empty
    for root, dirs, files in os.walk(image_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    async with aiohttp.ClientSession() as session:
        for i in range(len(json_shop['shop'])):

            # We need to avoid the situation where there are no photos
            if len(json_shop['shop'][i]['displayAssets']) != 0:

                # Get the number of assets per unique item (Most skins will have a BR and Lego image. We want the BR or Racing image).
                display_assets_length = len(json_shop['shop'][i]['displayAssets'])

                # Loop through the assets to get the BR or Racing image link.
                for j in range (0, display_assets_length):
                    if((json_shop['shop'][i]['displayAssets'][j]["primaryMode"] == "BattleRoyale") or (json_shop['shop'][i]['displayAssets'][j]["primaryMode"] == "DelMar")):
                        image_url = json_shop['shop'][i]['displayAssets'][j].get('full_background')
                        break

                if image_url:

                    # Create the image name
                    filename = os.path.join(image_path, f"shop_image_{i}.jpg")

                    # Fetch the image
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            # If we get the image, save it to the shop_images folder
                            async with aiofiles.open(filename, 'wb') as f:
                                await f.write(await response.read())

# Combine the shop images into one large image
async def create_shop_image(image_path):
    try:
        subprocess.run("combine_images.bat", shell = False)
        
    except subprocess.CalledProcessError as e:
        print(e)
        return e