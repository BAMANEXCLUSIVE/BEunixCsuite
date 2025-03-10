feedback_list = []

def collect_feedback(feedback):
    feedback_list.append(feedback)
    return "Feedback received!"

print(collect_feedback("Great service!"))