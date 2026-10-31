def categorize(description):

    description = str(description).lower()

    categories = {
        "Food": [
            "pizza",
            "dominos",
            "zomato",
            "swiggy",
            "restaurant",
            "burger"
        ],

        "Transport": [
            "uber",
            "ola",
            "fuel",
            "petrol",
            "diesel"
        ],

        "Shopping": [
            "amazon",
            "flipkart",
            "myntra"
        ],

        "Utilities": [
            "electricity",
            "internet",
            "water",
            "recharge",
            "bill"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in description:
                return category

    return "Other"