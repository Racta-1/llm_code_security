from urllib.parse import parse_qs

def parse_query_string(query):
    if not isinstance(query, str):
        raise TypeError(f"Expected a string, got {type(query).__name__}")

    if not query.strip():
        raise ValueError("Query string must not be empty or blank")

    parsed = parse_qs(
        query,
        keep_blank_values=True,
        strict_parsing=True,
        errors="strict",
    )

    empty_keys = [k for k in parsed if not k.strip()]
    if empty_keys:
        raise ValueError(f"Query string contains empty or blank parameter names")

    # Repeated keys: first value wins (documented behaviour)
    return {key: values[0] for key, values in parsed.items()}


# Example usage
if __name__ == "__main__":
    sample = "name=John&age=25&active=true"
    print(parse_query_string(sample))

    # URL-encoded characters
    print(parse_query_string("city=New%20York&lang=en"))

    # Repeated key — first value wins
    print(parse_query_string("x=1&x=2&x=3"))

    # Invalid cases
    for bad in [None, "   ", "&&", "=noname"]:
        try:
            print(parse_query_string(bad))
        except (TypeError, ValueError) as e:
            print(f"{type(e).__name__}: {e}")