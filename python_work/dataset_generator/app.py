from flask import Flask, render_template, request, send_file
from faker import Faker
import datetime
import csv

app=Flask(__name__)

@app.route('/')
# this function will display default webpage to user. whenever user hits url:
def home():
    return render_template('index.html')

@app.route('/submit', methods=['post'])

def submit():
    #define variables:
    
    fake=Faker()
    record_count=int(request.form['record_count'])
    
    def count_rows():
        with open(r'static/files/test_file.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            row_count = sum(1 for _ in reader)
        return row_count

    def open_csv_file():
        csv_file=open(r"static/files/test_file.csv", 'w')
        return csv_file

    def open_log_file():
        log_file=open(r"static/logs/log.txt", 'w')
        return log_file

    def file_open():
        open_csv_file()
        open_log_file()
        return 

    outfile=open_csv_file()
    outfile_logfile=open_log_file() 

    def generate_and_write_data(record_count):
        header='Name,Address,,City,State,Zipcode,Company,Job'
        outfile.write(header)
        details=[]
        for _ in range(record_count):
            details.append(fake.name())
            details.append(fake.address())
            details.append(fake.city())
            details.append(fake.state())
            details.append(fake.zipcode())
            details.append(fake.company())
            details.append(fake.job())
            outfile.write('\n')
            # coverted list into string:
            details_string=str(details)

            # formatting detailsstring such as remove prefix and suffix braket, remove quote mark.
            details_string=details_string.removeprefix('[')
            details_string=details_string.removesuffix(']')
            details_string=details_string.replace("'","")

            #writting formatted string to output file:
            outfile.write(details_string)
            
            #writing logs to log file:
            outfile_logfile.write('\n')
            outfile_logfile.write(str('Now writing:' + str(details)))

            # counter to count no of lines written
          

            #intialize list to append new data for next loop
            details=[]
        return 

    def write_log_header():
        date=('Log date: {}'.format(datetime.datetime.now()))
        file_name=('Opening file: '+str(outfile.name))
        outfile_logfile.write('*'*100)
        outfile_logfile.write('\n')
        outfile_logfile.write(date)
        outfile_logfile.write('\n')
        outfile_logfile.write(file_name)
        outfile_logfile.write('\n')
        outfile_logfile.write('*'*100)
        return
    


    def write_log_trailer():
        counter=record_count
        outfile_logfile.write('\n')
        outfile_logfile.write('*'*100)
        no_of_lines=('No of lines written: {}'.format(counter))
        outfile_logfile.write('\n')
        outfile_logfile.write(no_of_lines)
        outfile_logfile.write('\n')
        outfile_logfile.write('*'*100)
        return counter
    
    def close_file():
        outfile.close()
        outfile_logfile.close()
        return

    def main_function():
        file_open()
        write_log_header()
        generate_and_write_data(record_count)
        write_log_trailer()
        return 
    
    main_function()
    rows=count_rows()

    message=f'{record_count} records generated'
    return render_template('index.html', message=message, rows=rows)

@app.route('/download')
def download():
    # Replace 'dataset.csv' with your dataset file path
    file_path = 'static/files/test_file.csv'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)