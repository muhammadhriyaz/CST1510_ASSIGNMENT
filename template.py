def check_record(value, limit):
    difference = limit - value

    if limit != 0:
        percent = value / limit * 100
    else:
        percent = 0.0

    if value > limit:
        status = "OVER LIMIT"
    else:
        status = "OK"

    return difference, percent, status


def print_report(label, value, limit, difference, percent, status):
    print(
        f"{label}: loaded {value:,} / expected {limit:,}; "
        f"difference {difference:+,}; {percent:.1f}% — {status}"
    )


def print_message(message):
    print(message)


def load_records(path):
    records = []

    with open(path, "r") as file:
        for line in file:
            line = line.strip()

            if line != "":
                parts = line.split(",")

                record = {
                    "label": parts[0],
                    "value": int(parts[1]),
                    "limit": int(parts[2])
                }

                records.append(record)

    return records


def write_results(path, results):
    with open(path, "w") as file:
        for label, status in results:
            file.write(f"{label},{status}\n")


records = load_records(DATA_PATH)
results = []
over_limit_count = 0

for record in records:
    difference, percent, status = check_record(
        record["value"],
        record["limit"]
    )

    record["status"] = status

    print_report(
        record["label"],
        record["value"],
        record["limit"],
        difference,
        percent,
        status
    )

    results.append((record["label"], status))

    if status == "OVER LIMIT":
        over_limit_count += 1

write_results(RESULTS_PATH, results)

print_message(f"Datasets over expected rows: {over_limit_count}")
print_message(f"Results saved to {RESULTS_PATH.name}")