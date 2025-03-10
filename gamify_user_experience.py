def gamify_user_experience(points):
    if points >= 100:
        return "You've reached a new level!"
    return "Keep going!"

print(gamify_user_experience(120))