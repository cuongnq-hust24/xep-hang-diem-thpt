from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the data once when the app starts
data = pd.read_csv('diemthi2023.csv')

def tracuu(student_id, subject_combo):
    ma_tinh = int(str(student_id)[:2]) * 1000000

    sorted_toanquoc = data.sort_values(by=subject_combo, ascending=False)
    data_tinh = data.loc[(data.sbd >= ma_tinh) & (data.sbd < ma_tinh + 1000000)]
    sorted_tinh = data_tinh.sort_values(by=subject_combo, ascending=False)
    
    national_rank = np.where(sorted_toanquoc['sbd'].values == student_id)[0] + 1
    local_rank = np.where(sorted_tinh['sbd'].values == student_id)[0] + 1
    
    return {'national': national_rank[0] if len(national_rank) > 0 else None, 
            'local': local_rank[0] if len(local_rank) > 0 else None}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_combo = request.form['subject_combo']
        
        ranking = tracuu(int(student_id), subject_combo)
        
        return render_template('index.html', ranking=ranking, student_id=student_id, subject_combo=subject_combo)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
