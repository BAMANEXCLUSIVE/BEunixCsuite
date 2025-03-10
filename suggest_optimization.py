def suggest_optimization(current_performance):
    if current_performance < 70:
        return "Consider revising your strategy."
    return "Your strategy is performing well!"

print(suggest_optimization(65))