from flask import Flask, render_template, request, session
import os, subprocess

app = Flask(__name__)
app.secret_key = 'badcode'

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/sandhi_viched', methods=['POST'])
def sandhi_viched():
    text = request.form['sandhi_user_input']
    in_enc = request.form['in_enc']
    op_enc = request.form['op_enc']
    segmentation_mode = request.form['segmentation_mode']
    result_mode = request.form['result_mode']

    # Store the current state in the session
    session['sandhi_user_input'] = text
    session['sandhi_selected_encoding'] = in_enc
    session['sandhi_selected_output_encoding'] = op_enc
    session['sandhi_selected_segmentation_mode'] = segmentation_mode
    session['sandhi_selected_result_mode'] = result_mode

    command = f'python3 sandhi_vicchedika.py {in_enc} {op_enc} {segmentation_mode} {result_mode} -t "{text}"'
    print(command)
    processed_output = subprocess.run(command, shell=True, capture_output=True, text=True)
    session['sandhi_processed_output'] = processed_output.stdout

    return process_html()

@app.route('/pada_vishleshika', methods=['POST'])
def pada_vishleshika():
    user_input = request.form['pada_user_input']
    in_enc = request.form['in_enc']
    op_enc = request.form['op_enc']
    result_mode = request.form['result_mode']

    # Store the current state in the session
    session['pada_user_input'] = user_input
    session['pada_selected_encoding'] = in_enc
    session['pada_selected_output_encoding'] = op_enc
    session['pada_selected_result_mode'] = result_mode




    command = f'python3 pada_vishleshika.py {in_enc} {op_enc} {result_mode} -t "{user_input}"'
    processed_output = subprocess.run(command, shell=True, capture_output=True, text=True)
    session['pada_processed_output'] = processed_output.stdout

    return process_html()

def process_html():
    return render_template('index.html', sandhiViched=session.get('sandhi_processed_output', ''),
                           sandhi_selected_encoding=session.get('sandhi_selected_encoding', 'WX'),
                           sandhi_selected_output_encoding=session.get('sandhi_selected_output_encoding', 'deva'),
                           sandhi_selected_segmentation_mode=session.get('sandhi_selected_segmentation_mode', 'word'),
                           sandhi_selected_result_mode=session.get('sandhi_selected_result_mode', 'first'),
                           sandhi_user_input=session.get('sandhi_user_input', ''),

                           padaVishleshika=session.get('pada_processed_output', ''),
                           pada_selected_encoding=session.get('pada_selected_encoding', 'WX'),
                           pada_selected_output_encoding=session.get('pada_selected_output_encoding', 'deva'),
                           pada_selected_segmentation_mode=session.get('pada_selected_segmentation_mode', 'word'),
                           pada_selected_result_mode=session.get('pada_selected_result_mode', 'first'),
                           pada_user_input=session.get('pada_user_input', '')
                           )


if __name__ == '__main__':
    app.run(debug=True)