from flask import (Flask,
                   request,
                   redirect,
                   url_for,
                   g,
                   session,
                   render_template,
                   Response,
                   send_file)
import os
from analysis import *
from extract_data import *
from diagnose import *

app = Flask(__name__)
app.secret_key = 'secretkeyforadbmslabassignment'
app.url_map.strict_slashes = False
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['download'] = 'download'

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='me', password='csis123'))

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


@app.route('/')
def index():
    if not g.user:
        return redirect('/login')
    return redirect('/home')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = [x for x in users if x.username == username]
        if len(user):
            user = user[0]
        else:
            user = None

        if user and user.password==password:
            session['user_id'] = user.id
            return redirect('/home')
        else:
            return render_template('login_page.html', error = 'Incorrect login.')
    return render_template('login_page.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/home', methods=['GET'])
def home():
    if not g.user:
        return redirect('/login')
    return render_template('home_page.html')

@app.route('/analysis', methods=['GET'])
def analysis():
    if not g.user:
        return redirect('/login')
    return render_template('analysis.html')

@app.route('/analysis_summary', methods=['GET','POST'])
def analysis_summary():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path, diseaseDict = get_summary()
    else:
        img_path = '/image/summary.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis.html',header='Patient Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_malaria', methods=['GET','POST'])
def analysis_malaria():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_malaria()
    else:
        img_path = '/image/malaria.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_malaria.html',header='Malaria Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_pneumonia', methods=['GET','POST'])
def analysis_pneumonia():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_pneumonia()
    else:
        img_path = '/image/pneumonia.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_pneumonia.html',header='Pneumonia Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_depression', methods=['GET','POST'])
def analysis_depression():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_depression()
    else:
        img_path = '/image/depression.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_depression.html',header='Depression Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_covid', methods=['GET','POST'])
def analysis_covid():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_covid()
    else:
        img_path = '/image/covid.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_covid.html',header='Covid Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_diabetes', methods=['GET','POST'])
def analysis_diabetes():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_diabetes()
    else:
        img_path = '/image/diabetes.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_diabetes.html',header='Diabetes Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/analysis_heart_disease', methods=['GET','POST'])
def analysis_heart_disease():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        img_path = get_heart_disease()
    else:
        img_path = '/image/heart_disease.png'
        diseaseDict = dict({'Malaria': 495,
                       'Pneumonia': 445,
                       'Depression': 398,
                       'Covid': 337,
                       'Diabetes': 216,
                       'Heart Disease': 166,
                      })
    return render_template('analysis_heart_disease.html',header='Heart Disease Summary',img=img_path, disease_dict=diseaseDict)

@app.route('/patient_details/', methods=['GET'])
def patient_details():
    if not g.user:
        return redirect('/login')
    return render_template('patient_details.html', input_data=[], input_columns=[])

@app.route('/patient_details/<disease>', methods=['GET','POST'])
def patient_detail_view(disease):
    if not g.user:
        return redirect('/login')
    print("Inside details view")
    data = []
    column = []
    if disease == 'malaria':
        data, column = get_malaria_data()
    elif disease == 'pneumonia':
        data, column = get_pneumonia_data()
    elif disease == 'depression':
        data, column = get_depression_data()
    elif disease == 'covid':
        data, column = get_covid_data()
    elif disease == 'diabetes':
        data, column = get_diabetes_data()
    elif disease == 'heart_disease':
        data, column = get_heart_disease_data()
    else:
        data, column = [], []
    return render_template('patient_details.html',input_data = data, input_columns=column)

@app.route('/patient_details/<int:id>',methods=['GET'])
def patient_detailed_view(id):
    if not g.user:
        return redirect('/login')
    outDict = get_record(int(id))
    return render_template('patient_detailed.html',data=outDict)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    path=filename
    fname = path.split('/')[-1]
    t = fname.split('.')[-1]
    print(filename, fname, t)
    if t == 'csv':
        with open(os.path.curdir+'/download/'+path) as fp:
            csv = fp.read()
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":"attachment;filename="+fname})
    else:
        return send_file(
            os.path.curdir+'/download/'+path,
            mimetype="image/"+t
        )     


@app.route('/diagnose_patient', methods=['GET','POST'])
def diagnose_patient():
    if not g.user:
        return redirect('/login')
    if request.method == 'POST':
        # Get file data from form
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']

        # Save files to server
        if file1:
            file1.save('/home/ubuntu/usertest/covid/ml/' + file1.filename)
        if file2:
            file2.save('/home/ubuntu/usertest/malaria/ml/' + file2.filename)
        if file3:
            file3.save('/home/ubuntu/usertest/mentalhealth/' + file3.filename)
        
        # Get data from form
        #id = request.form.get('id')
        print('Uploaded files saved')
        id=random_number = random.randint(1000, 9999)
        age = request.form.get('age')
        gender = request.form.get('gender')
        bp=request.form.get('bp')
        cholestrol=request.form.get('cholestrol')
        glucose=request.form.get('glucose')
        insulin=request.form.get('insulin')
        maxhr=request.form.get('maxhr')
        thalium=request.form.get('thalium')
        fbs=request.form.get('fbs')
        chestpaintype=request.form.get('chestpaintype')
        bmi=request.form.get('bmi')
        skinthickness=request.form.get('skinthickness')
        diabetesp=request.form.get('diabetesp')
        vessels=request.form.get('vessels')
        ekg=request.form.get('ekg')
        enigma=request.form.get('enigma')
        pregencies=request.form.get('pregencies')
        stdp=request.form.get('stdp')
        slope=request.form.get('slope')
        isCovid="absence"
        isMalaria="absence"
        isDiabetes="absence"
        isDepression="absence"
        isHeartDisease="absence"
        isPnuemonia="absence"

        if file1:
            input_dir_covid = '/home/ubuntu/usertest/covid/'
            input_covid_img_gen = image_gen.flow_from_directory(input_dir_covid,
                                                target_size=image_shape_covid[:2],
                                                batch_size=1,
                                                color_mode='rgb',
                                                class_mode=None,
            )
            # Calling Covid Predictor function
            pred = covidPredict(input_covid_img_gen)
            print('Covid: ',pred)  
            alist=list(pred[0])
            if alist[0]>0.5:
                isCovid="presence"
            if alist[2]>0.5:
                isPnuemonia="presence"
            os.remove('/home/ubuntu/usertest/covid/ml/' + file1.filename)

        if file2:
            input_dir_malaria = '/home/ubuntu/usertest/malaria/'
            input_malaria_img_gen = image_gen.flow_from_directory(input_dir_malaria,
                                                target_size=image_shape_malaria[:2],
                                                batch_size=1,
                                                color_mode='rgb',
                                                class_mode=None,
            )
            pred = malariaPredict(input_malaria_img_gen)
            print('Malaria: ', pred)
            probMalaria = 1-pred # Prob that patient has malaria 
            probMalaria = list(probMalaria[0])
            if probMalaria[0] > 0.5:
                isMalaria="presence"
            os.remove('/home/ubuntu/usertest/malaria/ml/' + file2.filename)
    
        if file3:
            path='/home/ubuntu/usertest/mentalhealth/'
            depressPred = depressionPredition(path)
            print('Depression: ', depressPred)
            isDepression=depressPred
            os.remove('/home/ubuntu/usertest/mentalhealth/' + file3.filename)

        if pregencies and  glucose and bp and skinthickness and insulin and bmi and diabetesp and age:
            alist=['pregencies','glucose','bp','skinthickness','insulin','bmi','diabetesp','age']
            blist=[pregencies,glucose,bp,skinthickness,insulin,bmi,diabetesp,age]
            df = pd.DataFrame([blist], columns=alist)
            diaPred= diabetesPredict(df)
            isd=diaPred[0][1]
            if isd > 0.5:
                isDiabetes="presence"    
    
        if age and gender and chestpaintype and bp and cholestrol and fbs and ekg and maxhr and enigma and stdp and slope and vessels and thallium:
            alist=['age','gender','chestpaintype','bp','cholestrol','fbs','ekg','maxhr','enigma','stdp','slope','vessels','thallium']
            blist=[age,gender,chestpaintype,bp,cholestrol,fbs,ekg,maxhr,enigma,stdp,slope,vessels,thallium]
            df = pd.DataFrame([blist], columns=alist)
            heartPred= heartDiseasePredict(df)
            isHeartDisease=heartPred[0]
        
        result = dict()
        result['Covid'] = isCovid
        result['Pneumonia'] = isPnuemonia
        result['Depression'] = isDepression
        result['Malaria'] = isMalaria
        result['Diabetes'] = isDiabetes
        result['Heart Disease'] = isHeartDisease
        return render_template('diagnosis.html', results=result)
    
    return render_template('diagnose_patient.html')


if __name__ == '__main__':
    image_gen = ImageDataGenerator(rotation_range=20, # rotate the image 20 degrees
                               width_shift_range=0.10, # Shift the pic width by a max of 5%
                               height_shift_range=0.10, # Shift the pic height by a max of 5%
                               rescale=1/255, # Rescale the image by normalzing it.
                               shear_range=0.1, # Shear means cutting away part of the image (max 10%)
                               zoom_range=0.1, # Zoom in by 10% max
                               horizontal_flip=True, # Allo horizontal flipping
                               fill_mode='nearest' # Fill in missing pixels with the nearest filled value
                              )
    image_shape_malaria = (130,130,3)
    image_shape_covid = (514,514,3)
    app.run(debug=True,host='0.0.0.0',port=5000)

