import requests
import csv
import datetime

FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def get_file_lines(url):
    """Downloads CSV file and writes data to employee.csv"""
    response = requests.get(url, stream=True)
    result = response.text

    with open("employee.csv", "w") as f:
        f.write(result)   
        
def get_same_or_newer(start_date):
    """Returns the employees that started on the given date, or the closest one."""
    get_file_lines(FILE_URL)
    emp_dict = {}
    emp_group = []
    group = {}
    
    with open("employee.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Start Date'] >= str(start_date):
                emp_dict[row['Start Date']] = row['Name'] + " " + row['Surname']
                for item in emp_dict:
                    if item not in emp_group:
                        emp_group.append(item)
                for i in emp_group:
                    if i in emp_dict:
                        group[i] = [emp_dict[i]]
    return group

def print_list(start_date):
    result = get_same_or_newer(start_date)
    for key, value in result.items():
        row_date = datetime.datetime.strptime(key, '%Y-%m-%d')
        print("Started on {} : {}".format(row_date.strftime("%b %d, %Y"), value))
        
def main():
    start_date = get_start_date()
    print_list(start_date)
    
if __name__ == "__main__":
    main()