def adapt_content(user_data):
    if user_data['interest'] == 'technology':
        return "Latest Tech News"
    else:
        return "General News"

user_data = {'interest': 'technology'}
print(adapt_content(user_data))