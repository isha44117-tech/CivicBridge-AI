from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the AI model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")


def analyze_complaint(description, location):

    def ask_ai(question):
        inputs = tokenizer(question, return_tensors="pt")

        outputs = model.generate(
            **inputs,
            max_new_tokens=40
        )

        return tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()

    category = ask_ai(
        f"""Classify this civic complaint into exactly one category:
Waste Management, Road, Streetlight, Water, Traffic, Other.

Complaint: {description}

Answer with only the category name."""
    )

    priority = ask_ai(
        f"""Choose the priority of this civic complaint:
Low, Medium, or High.

Complaint: {description}

Answer with only one word."""
    )

    summary = f"Reported civic issue: {description.strip()}."


    

    authority = ask_ai(
    f"""You are a civic department classifier.

Complaint: {description}

Return EXACTLY ONE of these department names:
Municipal Corporation
Public Works Department
Water Supply Department
Electricity Department
Traffic Police
Other

For garbage, waste, litter, or sanitation complaints, return exactly:
Municipal Corporation

Return ONLY ONE department name."""
)

    return {
        "category": category,
        "priority": priority,
        "summary": summary,
        "authority": authority
    }