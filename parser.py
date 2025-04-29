import re

def parse_lab_report(text):
    lines = text.split('\n')
    results = []

    # Basic patterns
    value_pattern = re.compile(r'([-+]?[0-9]*\.?[0-9]+)')
    range_pattern = re.compile(r'([-+]?[0-9]*\.?[0-9]+)-([-+]?[0-9]*\.?[0-9]+)')

    current_test = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Example match: "HEMOGLOBIN 11.0 gm%"
        matches = value_pattern.findall(line)

        if matches:
            # Try to extract Test Name, Value and Unit
            parts = line.split()
            test_name = ' '.join(parts[:-2]).strip() if len(parts) >= 3 else line
            test_value = matches[0]
            test_unit = parts[-1] if len(parts) >= 2 else ''

            # Search for a reference range
            ref_match = range_pattern.search(line)
            if ref_match:
                lower = float(ref_match.group(1))
                upper = float(ref_match.group(2))
                bio_reference_range = f"{lower}-{upper}"
                lab_test_out_of_range = not (lower <= float(test_value) <= upper)
            else:
                bio_reference_range = ""
                lab_test_out_of_range = False

            results.append({
                "test_name": test_name,
                "test_value": test_value,
                "bio_reference_range": bio_reference_range,
                "test_unit": test_unit,
                "lab_test_out_of_range": lab_test_out_of_range
            })

    return results
