"""All personal-data matching and masking uses Python's standard re module."""
import re

RULES = {
    "credit": r"(?<![\w-])(?:[0-9]{4}-){3}[0-9]{4}(?![\w-])",
    "email": r"(?<![\w.!#$%&'*+/=?^`{|}~@-])[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![\w@-])",
    "phone": r"(?<![\w-])[0-9]{3}-[0-9]{3}-[0-9]{4}(?![\w-])",
    "dob": r"(?<!\w)(?i:DOB)[ \t]*:[ \t]*[0-9]{2}/[0-9]{2}/[0-9]{4}(?![\w/])",
    "address": r"(?<!\w)(?i:Address)[ \t]*:[ \t]*[0-9]+(?:[/-][0-9]+)*(?![\w/-])",
}
# A single substitution pass avoids masking text produced by another rule.
PATTERN = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in RULES.items()))


def mask_text(text):
    """Return masked text and number of recognized occurrences of each type.

    DOB is format matching, not calendar validation. Address masks only the
    house-number token after its label; the rest of the address is preserved.
    Short email usernames preserve their first/last characters literally.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    counts = dict.fromkeys(RULES, 0)

    def replace(match):
        kind, value = match.lastgroup, match.group()
        counts[kind] += 1
        if kind == "credit":
            return "XXXX-XXXX-XXXX-" + value[-4:]
        if kind == "phone":
            return "XXX-XXX-" + value[-4:]
        if kind == "email":
            user, domain = value.rsplit("@", 1)
            masked = user if len(user) <= 2 else user[0] + "*" * (len(user) - 2) + user[-1]
            return masked + "@" + domain
        if kind == "dob":
            return re.sub(r"[0-9]{2}/[0-9]{2}/([0-9]{2})[0-9]{2}$", r"XX/XX/\1XX", value)
        # Preserve the friend's original policy: one house number becomes XXX.
        return re.sub(r"[0-9]+(?:[/-][0-9]+)*$", "XXX", value)

    return {"text": PATTERN.sub(replace, text), "counts": counts}
