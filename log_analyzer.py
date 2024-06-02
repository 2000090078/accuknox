import re
from collections import defaultdict, Counter

# Function to parse a single log line
def parse_log_line(line):
    pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s.*\[(?P<date>.*?)\]\s"(?P<request>.*?)"\s(?P<status>\d+)\s(?P<size>\d+)'
    )
    match = pattern.match(line)
    if match:
        return match.groupdict()
    return None

# Function to analyze the log file
def analyze_log_file(filepath):
    requests = []
    status_counts = Counter()
    ip_counts = Counter()
    page_counts = Counter()

    with open(filepath, 'r') as file:
        for line in file:
            data = parse_log_line(line)
            if data:
                requests.append(data)
                status_counts[data['status']] += 1
                ip_counts[data['ip']] += 1

                request_parts = data['request'].split()
                if len(request_parts) > 1:
                    page_counts[request_parts[1]] += 1

    return {
        'total_requests': len(requests),
        'status_counts': status_counts,
        'ip_counts': ip_counts,
        'page_counts': page_counts,
    }

# Function to print the summary report
def print_summary(report):
    print("Summary Report")
    print("="*40)
    print(f"Total Requests: {report['total_requests']}")
    print("\nStatus Codes:")
    for status, count in report['status_counts'].items():
        print(f"  {status}: {count}")
    
    print("\nTop 10 Requested Pages:")
    for page, count in report['page_counts'].most_common(10):
        print(f"  {page}: {count}")
    
    print("\nTop 10 IP Addresses:")
    for ip, count in report['ip_counts'].most_common(10):
        print(f"  {ip}: {count}")

# Main function
def main():
    log_file_path = r'C:\Users\Murthy Nandula\Downloads\log_analyzer.py'  # Replace with the actual log file path
    report = analyze_log_file(log_file_path)
    print_summary(report)

if __name__ == "__main__":
    main()
