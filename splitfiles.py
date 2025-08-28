import csv

input_file = "datasets/partitioned_data/yellow_tripdata-part-4.csv"
rows_per_file = 100_000  # Adjust based on size, e.g., 500k rows per file

with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read header

    file_number = 1
    rows = []

    for row in reader:
        rows.append(row)
        if len(rows) >= rows_per_file:
            output_file = f"datasets/partitioned_data_small/yellow_tripdata-100k-{file_number}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(header)
                writer.writerows(rows)
            print(f"Written {output_file}")
            file_number += 1
            rows = []

    # Write remaining rows
    if rows:
        output_file = f"datasets/partitioned_data/yellow_tripdata-part-{file_number}.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Written {output_file}")
