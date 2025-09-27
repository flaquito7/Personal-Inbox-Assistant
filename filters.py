KEYWORDS = ["job", "interview", "reply", "offer", "opportunity", "hiring"]

def important(email):
    subject = email["subject"].lower()
    return any(k in subject for k in KEYWORDS)

