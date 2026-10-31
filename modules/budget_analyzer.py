def analyze_budget(df, budgets):

    report = []

    for category, budget in budgets.items():

        spent = df[df["Category"] == category]["Amount"].sum()

        remaining = budget - spent

        report.append({
            "Category": category,
            "Budget": budget,
            "Spent": spent,
            "Remaining": remaining
        })

    return report