import requests

base_url = "https://dev.erp.gotagid.com"    
login = "rao+odt@mlioncorp.com"
key = "a0f45d49451c4c560e2d755b89c08e12b2d93559"

def get_inventory_item():
    try:   
        response = requests.get(base_url, auth=(login, key), timeout=10)
        return response.json()
    except requests.exceptions.Timeout:
        print('The request timed out')
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Function to create a new inventory item
def create_inventory_item(data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(base_url, json=data, auth=(login, key), headers=headers)
    return response.json()

# Function to update an existing inventory item
def update_inventory_item(item_id, data):
    headers = {"Content-Type": "application/json"}
    response = requests.put(base_url, json=data, auth=(login, key), headers=headers)
    return response.json()

# Function to delete an inventory item
def delete_inventory_item(item_id):
    response = requests.delete(base_url, auth=(login, key))
    return response.json()


if __name__ == "__main__":
    
    data = {
        "name": "Steel Plates(100mm)",
        "length": 12,
        "height":12
    }

    # Update the retrieved item
    updated_data = {
        "name": "Updated Item",
        "quantity": 150,
        "price": 12.99
    }

    # Retrieve existing inventory items
    retrieved_item = get_inventory_item()
    print("Retrieved Item:", retrieved_item)

    # Create a new inventory item
    new_item = create_inventory_item(data)
    print("New Item:", new_item)

    
    item_id = new_item.get("id")
    if item_id:
        # Get the newly created item by ID
        updated_item = update_inventory_item(item_id, updated_data)
        print("Updated Item:", updated_item)
            

        # Delete the updated item
        deletion_result = delete_inventory_item(item_id)
        print("Deletion Result:", deletion_result)
