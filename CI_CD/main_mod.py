def main():
    data = get_collection(BASE_URL, API_KEY, COLLECTION_GUID)
    
    if data is None:
        print("Failed to retrieve collection data.")
        return
    
    if 'analytic_filter' not in data:
        print("No 'analytic_filter' found in the collection data.")
        return
    
    analytics = extract_values(data['analytic_filter'])
    attacks = extract_values(data['bsscript_filter'])
    threatevents = extract_values(data['sessions'])
    
    deployed = get_deployed(BASE_URL, API_KEY)
    
    if deployed is None:
        print("Failed to retrieve deployed data.")
        return
    
    deployed_guids = [item.get('guid') for item in deployed.get('items', [])]
    matches = [x for x in deployed_guids if x in analytics]
    print(matches)
    
    diff = [x for x in analytics if x not in deployed_guids]
    print(diff)

if __name__ == "__main__":
    main()
