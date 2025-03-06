def send_nudge(user_action):
    if user_action == 'abandoned_cart':
        return "Don't forget your items in the cart!"
    return "Welcome back!"

print(send_nudge('abandoned_cart'))