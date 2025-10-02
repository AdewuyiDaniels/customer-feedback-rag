import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_sample_data(num_entries=100):
    """
    Generates a CSV file with sample customer feedback data.
    """
    fake = Faker()
    data = []

    customer_segments = ["Enterprise", "SMB", "Startup"]
    source_types = ["review", "survey"]
    feedback_templates = {
        "feature_request": [
            "We would love to see an integration with {service}.",
            "A mobile app would be a game-changer for our team.",
            "The UI for the {feature} feature could be more intuitive.",
            "Can you please add support for {file_format} files?",
            "It would be great if we could customize the {aspect} of the dashboard."
        ],
        "bug_report": [
            "The app crashes every time I try to upload a {file_type} file.",
            "I'm getting a 500 error when I try to access the {page} page.",
            "The new update seems to have broken the {feature} functionality.",
            "My data is not syncing correctly between devices.",
            "The login page is not working on the {browser} browser."
        ],
        "pricing_concern": [
            "The pricing is a bit too high for a startup like ours.",
            "I'm confused about the billing structure. Can you clarify?",
            "Are there any discounts available for non-profit organizations?",
            "The cost of the {plan_name} plan is not justified by the features.",
            "We need a more flexible pricing plan for our seasonal business."
        ],
        "support_experience": [
            "The customer support team was very helpful and resolved my issue quickly.",
            "I was on hold for over an hour, and the support agent was not helpful.",
            "Your documentation is excellent and helped me solve the problem myself.",
            "The live chat support is a great feature.",
            "I never received a response to my support ticket."
        ],
        "positive_feedback": [
            "This product has been a lifesaver for our team. Thank you!",
            "I'm very impressed with the new features in the latest update.",
            "The user interface is so clean and easy to use.",
            "Your customer service is top-notch.",
            "I would highly recommend this product to anyone."
        ]
    }

    for i in range(num_entries):
        feedback_type = random.choice(list(feedback_templates.keys()))
        feedback_text_template = random.choice(feedback_templates[feedback_type])

        # Populate templates with fake data
        if feedback_type == "feature_request":
            feedback_text = feedback_text_template.format(
                service=fake.company(),
                feature=random.choice(["reporting", "analytics", "collaboration"]),
                file_format=random.choice(["PDF", "CSV", "XLSX"]),
                aspect=random.choice(["color scheme", "layout"])
            )
            rating = random.randint(3, 5)
        elif feedback_type == "bug_report":
            feedback_text = feedback_text_template.format(
                file_type=random.choice(["image", "video", "document"]),
                page=random.choice(["dashboard", "settings", "profile"]),
                feature=random.choice(["export", "import", "search"]),
                browser=random.choice(["Chrome", "Firefox", "Safari"])
            )
            rating = random.randint(1, 3)
        elif feedback_type == "pricing_concern":
            feedback_text = feedback_text_template.format(
                plan_name=random.choice(["Basic", "Pro", "Enterprise"])
            )
            rating = random.randint(2, 4)
        elif feedback_type == "support_experience":
            rating = random.choice([1, 2, 4, 5]) # Avoid neutral for support
            feedback_text = feedback_text_template
        else: # positive_feedback
            rating = 5
            feedback_text = feedback_text_template

        entry = {
            "feedback_id": i + 1,
            "customer_segment": random.choice(customer_segments),
            "feedback_text": feedback_text,
            "rating": rating,
            "date": fake.date_between(start_date="-90d", end_date="today"),
            "source_type": random.choice(source_types)
        }
        data.append(entry)

    df = pd.DataFrame(data)
    df.to_csv("data/sample_feedback.csv", index=False)
    print(f"{num_entries} sample feedback entries have been generated and saved to 'data/sample_feedback.csv'.")


if __name__ == "__main__":
    generate_sample_data()