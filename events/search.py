def make_search(query_string, event_list=[]):
    query_string = query_string.lower()
    query_words = query_string.split()  # get the contents of the search bar and split it up by word
    # some words may result in many entries being found because the word is common. Stop words hopes to eliminate that
    stop_words = ["a", "and", "the", "where", "how", "what", "or", 'i', 'a']
    for word in query_words:  # remove stop words from the input
        if word in stop_words:
            query_words.remove(word)

    found_entries = []  # by default found entries is empty
    # Check every event for a match in the title, description, or location
    for event in event_list:
        if event.title.lower() is query_string:
            found_entries.append(event)
        elif query_string in event.title.lower():
            found_entries.append(event)
        elif query_string in event.desc.lower():
            found_entries.append(event)
        elif query_string in event.location_name.lower():
            found_entries.append(event)
    return found_entries
