import sys
import csv
import os

def read_grades(file_path):
    """Reads CSV data and returns student names and their grades"""
    students = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["Student"]
                grades = [int(row[subject]) for subject in reader.fieldnames[1:]]
                students.append((name, grades))
        return students, reader.fieldnames[1:]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

def calculate_averages(students):
    """Calculates average grade per student"""
    return {name: sum(grades)/len(grades) for name, grades in students}

def calculate_highest_per_subject(students, subjects):
    """Finds the highest grade for each subject"""
    subject_max = [0]*len(subjects)
    for _, grades in students:
        for i in range(len(grades)):
            if grades[i] > subject_max[i]:
                subject_max[i] = grades[i]
    return dict(zip(subjects, subject_max))

def write_report_txt(averages, highest_scores, output_file):
    """Writes results to a TXT file"""
    with open(output_file, 'w') as f:
        f.write("Student Averages:\n")
        for student, avg in averages.items():
            f.write(f"{student}: {avg:.2f}\n")

        f.write("\nHighest Scores per Subject:\n")
        for subject, score in highest_scores.items():
            f.write(f"{subject}: {score}\n")

def write_summary_csv(averages, highest_scores, output_file):
    """Writes results to a CSV file"""
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Student", "Average"])
        for student, avg in averages.items():
            writer.writerow([student, f"{avg:.2f}"])

        writer.writerow([])  # Empty row
        writer.writerow(["Subject", "Highest Score"])
        for subject, score in highest_scores.items():
            writer.writerow([subject, score])

def main():
    if len(sys.argv) != 2:
        print("Usage: python processor.py data/grades.csv")
        sys.exit(1)

    input_path = sys.argv[1]
    output_txt = "output/report.txt"
    output_csv = "output/summary.csv"

    students, subjects = read_grades(input_path)
    averages = calculate_averages(students)
    highest_scores = calculate_highest_per_subject(students, subjects)
    
    write_report_txt(averages, highest_scores, output_txt)
    write_summary_csv(averages, highest_scores, output_csv)

    print(f"Report generated:\nTXT: {output_txt}\nCSV: {output_csv}")

if __name__ == "__main__":
    main()
