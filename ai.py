from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the AI model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")


def analyze_complaint(description, location):
    text = description.lower().strip()

    # Category detection
    if any(word in text for word in [
        "garbage", "waste", "trash", "litter", "rubbish",
        "dustbin", "sanitation", "dump"
    ]):
        category = "Waste Management"

    elif any(word in text for word in [
        "pothole", "road", "street damage", "broken road",
        "crack in road", "damaged road"
    ]):
        category = "Road"

    elif any(word in text for word in [
        "streetlight", "street light", "light pole",
        "lamp post", "no lights", "lights not working"
    ]):
        category = "Streetlight"

    elif any(word in text for word in [
        "water leakage", "water leak", "water pipeline",
        "pipe burst", "water supply", "no water",
        "water shortage", "drainage", "sewage",
        "leaking pipe", "water is leaking"
    ]):
        category = "Water"

    elif any(word in text for word in [
        "traffic", "traffic jam", "signal", "accident",
        "congestion", "parking"
    ]):
        category = "Traffic"

    else:
        category = "Other"

    # Priority detection
    if any(word in text for word in [
        "emergency", "dangerous", "major", "severe",
        "accident", "burst pipe", "flooding","large pothole","deep pothole","major pothole","road collapsed"
    ]):
        priority = "High"

    elif any(word in text for word in [
        "not working", "blocked", "leaking",
        "broken", "overflow", "urgent","pothole","crack in road"
    ]):
        priority = "Medium"

    else:
        priority = "Low"

    # Summary
    summary = f"Reported civic issue: {description.strip()}."

    # Suggested authority
    if category == "Waste Management":
        authority = "Municipal Corporation"

    elif category == "Road":
        authority = "Public Works Department"

    elif category == "Streetlight":
        authority = "Electricity Department"

    elif category == "Water":
        authority = "Water Supply Department"

    elif category == "Traffic":
        authority = "Traffic Police"

    else:
        authority = "Other"

    return {
        "category": category,
        "priority": priority,
        "summary": summary,
        "authority": authority
    }