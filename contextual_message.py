def contextual_message(location):
    if location == 'home':
        return "Welcome back home!"
    return "Welcome!"

print(contextual_message('home'))