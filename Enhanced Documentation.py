def detect_new_elements(existing_elements, current_elements):
    new_elements = set(current_elements) - set(existing_elements)
    
    if new_elements:
        print("New elements detected:", new_elements)
        check_and_create_version()  # Trigger documentation creation if new elements are found

existing_elements = ['extract', 'transform', 'load']  # Example existing elements
current_elements = ['extract', 'transform', 'load', 'validate']  # Current elements including new ones

detect_new_elements(existing_elements, current_elements)