"""festreg.cleaner: validate and de-duplicate registrations."""


def valid_email(email):
    """String methods only: one @, non-empty local part, dotted domain."""
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain and not domain.startswith(".") \
        and not domain.endswith(".") and " " not in email


def parse_line(line):
    """regno,name,dept,email,event1;event2 -> dict, or raise ValueError."""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise ValueError(f"expected 5 fields, found {len(parts)}")
    reg, name, dept, email, events = parts
    if not reg or not name:
        raise ValueError("register number and name are required")
    if not valid_email(email):
        raise ValueError(f"invalid e-mail {email!r}")
    event_list = [e for e in (x.strip() for x in events.split(";")) if e]
    if not event_list:
        raise ValueError("no events chosen")
    return {"reg": reg, "name": name, "dept": dept, "email": email, "events": event_list}
