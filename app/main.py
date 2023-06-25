import psycopg2
import pandas as pd
import psycopg2.extras as extras
import csv
import time 
import redis
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField, HiddenField, SelectField, IntegerField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, join, func, Numeric, cast, Integer


print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#function for inserting data
def execute_values_with_index(conn, df, num_rows, start_ind_database=0, start_ind=0, step=5000):
    cursor = conn.cursor()
    
    index_currently = start_ind_database
    
    while start_ind_database < num_rows:
        # Get the current batch of rows
        batch_end_index = min(start_ind + step, num_rows)
        batch_df = df.iloc[start_ind:batch_end_index].copy()
        tuples = [tuple(x) for x in batch_df.to_numpy()]
        
        # Create the INSERT query with values for the values
        cols = ','.join(list(batch_df.columns))
        query = "INSERT INTO zno_results (%s) VALUES %%s ON CONFLICT (OUTID, YearTest) DO NOTHING;" % (cols)
        
        # Execute the INSERT query with the current batch of rows
        extras.execute_values(cursor, query, tuples)
        try:
            conn.commit()
        except:
            print("can't execute")
        # Update the batch start index and index
        start_ind += step
        start_ind_database += step
        index_currently += len(batch_df)
        
        # Print progress message
        print(f"Inserted {index_currently} rows.")
        
    # Commit the transaction and clean up
    cursor.close()

conn = psycopg2.connect(dbname="database", user="postgres", password="postgres", host="db")

while True:
    try:
        #checking connection
        cursor = conn.cursor()

        #creating table
        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS zno_results(
            OUTID varchar NOT NULL, 
            Birth integer, 
            SexTypeName varchar, 
            RegName varchar, 
            AREANAME varchar, 
            TERNAME varchar, 
            RegTypeName varchar, 
            TerTypeName varchar, 
            ClassProfileNAME varchar, 
            ClassLangName varchar, 
            EONAME varchar, 
            EOTypeName varchar, 
            EORegName varchar, 
            EOAreaName varchar, 
            EOTerName varchar, 
            EOParent varchar, 
            UMLTest varchar, 
            UMLTestStatus varchar, 
            UMLBall100 float, 
            UMLBall12 float, 
            UMLBall float, 
            UMLAdaptScale varchar, 
            UMLPTName varchar, 
            UMLPTRegName varchar, 
            UMLPTAreaName varchar, 
            UMLPTTerName varchar, 
            UkrTest varchar, 
            UkrSubTest varchar, 
            UkrTestStatus varchar, 
            UkrBall100 float, 
            UkrBall12 float, 
            UkrBall float, 
            UkrAdaptScale varchar, 
            UkrPTName varchar, 
            UkrPTRegName varchar, 
            UkrPTAreaName varchar, 
            UkrPTTerName varchar, 
            HistTest varchar, 
            HistLang varchar, 
            HistTestStatus varchar, 
            HistBall100 float, 
            HistBall12 float, 
            HistBall float, 
            HistPTName varchar, 
            HistPTRegName varchar, 
            HistPTAreaName varchar, 
            HistPTTerName varchar, 
            MathTest varchar, 
            MathLang varchar, 
            MathTestStatus varchar, 
            MathBall100 float, 
            MathBall12 float, 
            MathDPALevel varchar, 
            MathBall float, 
            MathPTName varchar, 
            MathPTRegName varchar, 
            MathPTAreaName varchar, 
            MathPTTerName varchar, 
            MathStTest varchar, 
            MathStLang varchar, 
            MathStTestStatus varchar, 
            MathStBall12 float, 
            MathStBall float, 
            MathStPTName varchar, 
            MathStPTRegName varchar, 
            MathStPTAreaName varchar, 
            MathStPTTerName varchar, 
            PhysTest varchar, 
            PhysLang varchar, 
            PhysTestStatus varchar, 
            PhysBall100 float, 
            PhysBall12 float, 
            PhysBall float, 
            PhysPTName varchar, 
            PhysPTRegName varchar, 
            PhysPTAreaName varchar, 
            PhysPTTerName varchar, 
            ChemTest varchar, 
            ChemLang varchar, 
            ChemTestStatus varchar, 
            ChemBall100 float, 
            ChemBall12 float, 
            ChemBall float, 
            ChemPTName varchar,
            ChemPTRegName varchar, 
            ChemPTAreaName varchar, 
            ChemPTTerName varchar, 
            BioTest varchar, 
            BioLang varchar, 
            BioTestStatus varchar, 
            BioBall100 float, 
            BioBall12 float, 
            BioBall float, 
            BioPTName varchar, 
            BioPTRegName varchar, 
            BioPTAreaName varchar, 
            BioPTTerName varchar, 
            GeoTest varchar, 
            GeoLang varchar, 
            GeoTestStatus varchar, 
            GeoBall100 float, 
            GeoBall12 float, 
            GeoBall float, 
            GeoPTName varchar, 
            GeoPTRegName varchar, 
            GeoPTAreaName varchar,
            GeoPTTerName varchar, 
            EngTest varchar, 
            EngTestStatus varchar, 
            EngBall100 float, 
            EngBall12 float, 
            EngDPALevel varchar, 
            EngBall float, 
            EngPTName varchar, 
            EngPTRegName varchar, 
            EngPTAreaName varchar, 
            EngPTTerName varchar, 
            FraTest varchar, 
            FraTestStats varchar, 
            FraBall100 float, 
            FraBall12 float, 
            FraDPALevel varchar, 
            FraBall float, 
            FraPTName varchar, 
            FraPTRegName varchar, 
            FraPTAreaName varchar, 
            FraPTTerName varchar, 
            DeuTest varchar,
            DeuTestStatus varchar, 
            DeuBall100 float, 
            DeuBall12 float, 
            DeuDPALevel varchar, 
            DeuBall float, 
            DeuPTName varchar, 
            DeuPTRegName varchar, 
            DeuPTAreaName varchar, 
            DeuPTTerName varchar, 
            SpaTest varchar, 
            SpaTestStatus varchar, 
            SpaBall100 float, 
            SpaBall12 float, 
            SpaDPALevel varchar, 
            SpaBall float, 
            SpaPTName varchar, 
            SpaPTRegName varchar, 
            SpaPTAreaName varchar, 
            SpaPTTerName varchar,
            YearTest integer
            );"""
        )

        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_OUTID_zno_results ON zno_results(OUTID, YearTest);")     

        #lists of columns for evry database
        l2021 = ['OUTID', 'Birth', 'SexTypeName', 'RegName', 'AREANAME', 'TERNAME', 'RegTypeName', 'TerTypeName', 'ClassProfileNAME', 'ClassLangName', 'EONAME', 'EOTypeName', 'EORegName', 'EOAreaName', 'EOTerName', 'EOParent', 'UMLTest', 'UMLTestStatus', 'UMLBall100', 'UMLBall12', 'UMLBall', 'UMLAdaptScale', 'UMLPTName', 
            'UMLPTRegName', 'UMLPTAreaName', 'UMLPTTerName', 'UkrTest', 'UkrSubTest', 'UkrTestStatus', 'UkrBall100', 'UkrBall12', 'UkrBall', 'UkrAdaptScale', 'UkrPTName', 'UkrPTRegName', 'UkrPTAreaName', 'UkrPTTerName', 'HistTest', 'HistLang', 'HistTestStatus', 'HistBall100', 'HistBall12', 'HistBall', 'HistPTName', 
            'HistPTRegName', 'HistPTAreaName', 'HistPTTerName', 'MathTest', 'MathLang', 'MathTestStatus', 'MathBall100', 'MathBall12', 'MathDpaLevel', 'MathBall', 'MathPTName', 'MathPTRegName', 'MathPTAreaName', 'MathPTTerName', 'MathStTest', 'MathStLang', 'MathStTestStatus', 'MathStBall12', 'MathStBall', 'MathStPTName', 
            'MathStPTRegName', 'MathStPTAreaName', 'MathStPTTerName', 'PhysTest', 'PhysLang', 'PhysTestStatus', 'PhysBall100', 'PhysBall12', 'PhysBall', 'PhysPTName', 'PhysPTRegName', 'PhysPTAreaName', 'PhysPTTerName', 'ChemTest', 'ChemLang', 'ChemTestStatus', 'ChemBall100', 'ChemBall12', 'ChemBall', 'ChemPTName',
            'ChemPTRegName', 'ChemPTAreaName', 'ChemPTTerName', 'BioTest', 'BioLang', 'BioTestStatus', 'BioBall100', 'BioBall12', 'BioBall', 'BioPTName', 'BioPTRegName', 'BioPTAreaName', 'BioPTTerName', 'GeoTest', 'GeoLang', 'GeoTestStatus', 'GeoBall100', 'GeoBall12', 'GeoBall', 'GeoPTName', 'GeoPTRegName', 'GeoPTAreaName',
            'GeoPTTerName', 'EngTest', 'EngTestStatus', 'EngBall100', 'EngBall12', 'EngDPALevel', 'EngBall', 'EngPTName', 'EngPTRegName', 'EngPTAreaName', 'EngPTTerName', 'FraTest', 'FraTestStats', 'FraBall100', 'FraBall12', 'FraDPALevel', 'FraBall', 'FraPTName', 'FraPTRegName', 'FraPTAreaName', 'FraPTTerName', 'DeuTest',
            'DeuTestStatus', 'DeuBall100', 'DeuBall12', 'DeuDPALevel', 'DeuBall', 'DeuPTName', 'DeuPTRegName', 'DeuPTAreaName', 'DeuPTTerName', 'SpaTest', 'SpaTestStatus', 'SpaBall100', 'SpaBall12', 'SpaDPALevel', 'SpaBall', 'SpaPTName', 'SpaPTRegName', 'SpaPTAreaName', 'SpaPTTerName']

        l2020 = ['OUTID', 'Birth', 'SexTypeName', 'RegName', 'AREANAME', 'TERNAME', 'RegTypeName', 'TerTypeName', 'ClassProfileNAME', 'ClassLangName', 'EONAME', 'EOTypeName', 'EORegName', 'EOAreaName', 'EOTerName', 'EOParent', 'UkrTest', 'UkrTestStatus', 'UkrBall100', 'UkrBall12', 'UkrBall', 'UkrAdaptScale', 'UkrPTName', 'UkrPTRegName',
            'UkrPTAreaName', 'UkrPTTerName', 'HistTest', 'HistLang', 'HistTestStatus', 'HistBall100', 'HistBall12', 'HistBall', 'HistPTName', 'HistPTRegName', 'HistPTAreaName', 'HistPTTerName', 'MathTest', 'MathLang', 'MathTestStatus', 'MathBall100', 'MathBall12', 'MathBall', 'MathPTName', 'MathPTRegName', 'MathPTAreaName', 'MathPTTerName', 
            'PhysTest', 'PhysLang', 'PhysTestStatus', 'PhysBall100', 'PhysBall12', 'PhysBall', 'PhysPTName', 'PhysPTRegName', 'PhysPTAreaName', 'PhysPTTerName', 'ChemTest', 'ChemLang', 'ChemTestStatus', 'ChemBall100', 'ChemBall12', 'ChemBall', 'ChemPTName',
            'ChemPTRegName', 'ChemPTAreaName', 'ChemPTTerName', 'BioTest', 'BioLang', 'BioTestStatus', 'BioBall100', 'BioBall12', 'BioBall', 'BioPTName', 'BioPTRegName', 'BioPTAreaName', 'BioPTTerName', 'GeoTest', 'GeoLang', 'GeoTestStatus', 'GeoBall100', 'GeoBall12', 'GeoBall', 'GeoPTName', 'GeoPTRegName', 'GeoPTAreaName',
            'GeoPTTerName', 'EngTest', 'EngTestStatus', 'EngBall100', 'EngBall12', 'EngDPALevel', 'EngBall', 'EngPTName', 'EngPTRegName', 'EngPTAreaName', 'EngPTTerName', 'FraTest', 'FraTestStats', 'FraBall100', 'FraBall12', 'FraDPALevel', 'FraBall', 'FraPTName', 'FraPTRegName', 'FraPTAreaName', 'FraPTTerName', 'DeuTest',
            'DeuTestStatus', 'DeuBall100', 'DeuBall12', 'DeuDPALevel', 'DeuBall', 'DeuPTName', 'DeuPTRegName', 'DeuPTAreaName', 'DeuPTTerName', 'SpaTest', 'SpaTestStatus', 'SpaBall100', 'SpaBall12', 'SpaDPALevel', 'SpaBall', 'SpaPTName', 'SpaPTRegName', 'SpaPTAreaName', 'SpaPTTerName']

        #reading data
        #df2021 = pd.read_csv("Odata2021File.csv", encoding='utf-8', delimiter=';', header=None, skiprows=[0], names = l2021)
        df2020 = pd.read_csv("Odata2020File.csv", encoding='windows-1251', delimiter=';', header=None, skiprows=[0], names = l2020)

        #adding year of the test to data
        df2020["YearTest"] = [2020 for _ in range(len(df2020))]
        #df2021["YearTest"] = [2021 for _ in range(len(df2021))]

        #changing the type of the balls100 columns
        for col in ['UMLBall100', 'UkrBall100', 'HistBall100', 'MathBall100', 'PhysBall100', 'ChemBall100', 'BioBall100', 'GeoBall100', 'EngBall100', 'FraBall100', 'DeuBall100', 'SpaBall100']:
            if col in list(df2020.columns):
                df2020[col] = df2020[col].str.replace(',','.', regex=True).astype(float)
            #df2021[col] = df2021[col].str.replace(',','.', regex=True).astype(float)

        #countimg time of inserting data
        start_time = time.time()
        execute_values_with_index(conn, df2020, 10000)
#        execute_values_with_index(conn, df2021, len(df2021)+len(df2020), len(df2020)-1)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("ready")

        #writing the file with time of inserting
        with open('time.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["The duration of inserting data is {}".format(elapsed_time)])
            print("good")
            csvfile.close()


        print("done")

    except psycopg2.OperationalError as err:
        print("error connection")
        for i in range(15):
            try:
                conn = psycopg2.connect(dbname="database", user="postgres", password="postgres", host="db")
                break
            except:
                print("no connection")
                time.sleep(20)
    else:
        break


app = Flask(__name__)
app.secret_key = 'Postavte30'

#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

username = 'postgres'
password = 'postgres'
database = 'database'
host = 'db'
dbms = 'postgres'

redis_url = 'redis://redis:6379/0'
redisClient = redis.from_url(redis_url)
CACHELIFETIME = 360

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{password}@{host}:5432/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# *******************************
# ORM mapping
# *******************************


#######################

class DBMSForm(FlaskForm):
    dbms = SelectField('DBMS', validators=[validators.DataRequired()], coerce=str)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(DBMSForm, self).__init__(*args, **kwargs)
        self.dbms.choices = ['mongodb', 'postgres']




class living_areaForm(FlaskForm):
    living_area_id = HiddenField()
    regname = StringField('RegName', validators=[validators.DataRequired("Please enter your field")])
    areaname = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    tername = StringField('TerName', validators=[validators.DataRequired("Please enter your field")])
    regtypename = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    tertypename = StringField('TerName', validators=[validators.DataRequired("Please enter your field")])
    submit = SubmitField("Submit")

class schoolForm(FlaskForm):
    eo_id = HiddenField('School ID')
    eoname = StringField('Name', validators=[validators.DataRequired("Please enter your field")])
    eotypename = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    eoregname = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    eoareaname = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    eotername = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    eoparent = StringField('Parentname', validators=[validators.DataRequired("Please enter your field")])
    submit = SubmitField("Submit")


class test_locationForm(FlaskForm):
    test_loc_id = HiddenField()
    ptname = StringField('Name', validators=[validators.DataRequired("Please enter your field")])
    ptregname = StringField('RegName', validators=[validators.DataRequired("Please enter your field")])
    ptareaname = StringField('AreaName', validators=[validators.DataRequired("Please enter your field")])
    pttername  = StringField('TerName', validators=[validators.DataRequired("Please enter your field")])
    submit = SubmitField("Submit")

class StudentForm(FlaskForm):
    outid = StringField('Student id')
    yeartest = IntegerField('ExamYear')
    birth = IntegerField('BirthDate')
    sextypename = StringField('Sex', validators=[validators.DataRequired("Please enter your field")])
    classprofilename = StringField('ClassProfile')
    classlangname = StringField('ClassLang')
    living_area_id = IntegerField('living_area', validators=[validators.DataRequired("Please enter your field")])
    eo_id = IntegerField('School', validators=[validators.DataRequired("Please enter your field")])
    submit = SubmitField("Submit")

    '''def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.living_area_id.choices = [
            (int(Living_area.living_area_id), f"{Living_area.regname}, {Living_area.areaname}, {Living_area.tername}, {Living_area.regtypename}, {Living_area.tertypename}") for Living_area in
            Living_area.query.all()]

        self.eo_id.choices = [
            (int(school.eo_id), f"{school.eoname}, {school.eotypename}, {school.eoregname}, {school.eoareaname}, {school.eotername}, {school.eoparent}") for school in
            School.query.all()]'''

    def validate(self):
        if not super(StudentForm, self).validate():
            return False
        living_area_id = self.living_area_id.data
        living_area = Living_area.query.get(living_area_id)
        if not living_area:
            self.living_area_id.errors.append('Invalid living_area')
            return False
        eo_id = self.eo_id.data
        school = School.query.get(eo_id)
        if not school:
            self.eo_id.errors.append('Invalid school')
            return False
        return True


class TestForm(FlaskForm):
    student_id = StringField('Student id', validators=[validators.DataRequired()])
    yeartest = IntegerField('YearTest', validators=[validators.DataRequired()])
    test_name = StringField('test name', validators=[validators.DataRequired()])
    lang = StringField('Lang')
    subtest = StringField('SubTest')
    teststatus = StringField('TestStatus')
    ball100 = DecimalField('Ball100', validators=[validators.DataRequired()])
    ball12 = IntegerField('Ball12', validators=[validators.DataRequired()])
    ball = IntegerField('Ball', validators=[validators.DataRequired()])
    adaptscale = IntegerField('AdaptScale', validators=[validators.DataRequired()])
    dpalevel = StringField('DPALevel')
    test_loc_id = IntegerField('test location id', validators=[validators.DataRequired()])
    submit = SubmitField("Submit")

    '''def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)

        self.student_id.choices = [
            (str(student.outid), f"{student.yeartest}, {student.birth}, {student.sextypename}, {student.classprofilename} \n"
                                      f"{student.classlangname}, {student.living_area_id}, {student.eo_id} ")
            for student in Student.query.all()]

        self.yeartest.choices = [
            (int(student.yeartest),
             f"{student.outid}, {student.birth}, {student.sextypename}, {student.classprofilename} \n"
             f"{student.classlangname}, {student.living_area_id}, {student.eo_id} ")
            for student in Student.query.all()]

        self.test_loc_id.choices = [
            (int(Test_loc.test_loc_id), f"{Test_loc.ptname}, {Test_loc.ptregname}, {Test_loc.ptareaname}, {Test_loc.pttername}") for Test_loc in
            Test_loc.query.all()]'''

    def validate(self):
        if not super(TestForm, self).validate():
            return False
        
        student_id = self.student_id.data
        student = Student.query.get(student_id)
        if not student:
            self.student_id.errors.append('Invalid student')
            return False

        yeartest = self.yeartest.data
        year = Student.query.filter_by(yeartest=yeartest).first()
        if not year:
            self.yeartest.errors.append('Invalid year')
            return False

        test_location_id = self.test_loc_id.data
        test = Test_loc.query.get(test_location_id)
        if not test:
            self.school_id.errors.append('Invalid test location')
            return False

        return True


class QueryForm(FlaskForm):
    regname = SelectMultipleField('Region Name', validators=[validators.DataRequired()], coerce=str)
    yeartest = SelectField('Year of the test', validators=[validators.DataRequired()], coerce=int)
    test_name = SelectField('Subject name', validators=[validators.DataRequired()], coerce=str)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)

        regions = [(living_area.regname, living_area.regname) for living_area in
                   Living_area.query.with_entities(Living_area.regname).distinct()]
        regions.insert(0, ('all', 'Усі регіони'))
        self.regname.choices = regions

        self.yeartest.choices = [(student.yeartest, student.yeartest) for student in
                                 Student.query.with_entities(Student.yeartest).distinct()]
        self.test_name.choices = [(subject.test_name, subject.test_name) for subject in
                                  Test.query.with_entities(Test.test_name).distinct()]


@app.route('/')
def index():
    table_names = ['Student', 'Tests', 'living_area', 'school', 'test_location']
    return render_template('index.html', table_names=table_names)


@app.route('/dbms', methods=['GET', 'POST'])
def DBMS():
    form = DBMSForm(request.form)
    global dbms
    dbms = form.dbms.data

    return render_template('choose_database_type.html', form=form, dbms=dbms)




@app.route('/<table_name>')
def show_table(table_name):
    page = int(request.args.get('page', 1))
    per_page = 50  # Number of rows per page

    if table_name == 'Student':
        query = db.session.query(Student).order_by(Student.outid)
        table_data = query.paginate(page=page, per_page=per_page)
        columns = Student.__table__.columns.keys()
        return render_template('show_table_student.html', table_name=table_name, table_data=table_data, columns=columns)
    elif table_name == 'Tests':
        query = db.session.query(Test).order_by(Test.student_id)
        table_data = query.paginate(page=page, per_page=per_page)
        columns = Test.__table__.columns.keys()
        return render_template('show_table_test.html', table_name=table_name, table_data=table_data, columns=columns)
    elif table_name == 'school':
        query = db.session.query(School).order_by(School.eo_id)
        table_data = query.paginate(page=page, per_page=per_page)
        columns = School.__table__.columns.keys()
        return render_template('show_table_school.html', table_name=table_name, table_data=table_data, columns=columns)
    elif table_name == 'living_area':
        query = db.session.query(Living_area).order_by(Living_area.living_area_id)
        table_data = query.paginate(page=page, per_page=per_page)
        columns = Living_area.__table__.columns.keys()
        return render_template('show_table_living_area.html', table_name=table_name, table_data=table_data, columns=columns)
    elif table_name == 'test_location':
        query = db.session.query(Test_loc).order_by(Test_loc.test_loc_id)
        table_data = query.paginate(page=page, per_page=per_page)
        columns = Test_loc.__table__.columns.keys()
        return render_template('show_table_test_loc.html', table_name=table_name, table_data=table_data, columns=columns)

@app.route('/school/insert', methods=['GET', 'POST'])
def addSchool():
    form = schoolForm(request.form)

    if request.method == 'POST':
        newSchool = School(
            # eo_id = db.Column(db.Integer, primary_key=True)
            eoname=form.eoname.data,
            eotypename=form.eotypename.data,
            eoregname=form.eoregname.data,
            eoareaname=form.eoareaname.data,
            eotername=form.eotername.data,
            eoparent=form.eoparent.data
        )
#        db.session.add(newSchool)
#        db.session.commit()

        redisClient.flushall()

        #new_school = School.query.filter_by(eo_id=newSchool.eo_id).first()
        #schools = School.query.filter(School.eo_id != newSchool.eo_id).all()
        #schools.insert(0, new_school)
        #columns = School.__table__.columns.keys()

        return redirect(url_for('show_table', table_name='school', page=1))

    return render_template('insert_row_school.html', form=form, action='addSchool')


@app.route('/Student/insert', methods=['GET', 'POST'])
def addStudents():
    form = StudentForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('insert_row_student.html', form=form, action='addStudents')

        newStudent = Student(
            outid=form.outid.data,
            yeartest=form.yeartest.data,
            birth=form.birth.data,
            sextypename=form.sextypename.data,
            classprofilename=form.classprofilename.data,
            classlangname=form.classlangname.data,
            living_area_id=form.living_area_id.data,
            eo_id=form.eo_id.data
        )
#        db.session.add(newStudent)
#        db.session.commit()

        redisClient.flushall()

        #new_student = Student.query.filter_by(outid=newStudent.outid).first()
        #students = Student.query.filter(Student.outid != newStudent.outid).all()
        #students.insert(0, new_student)
        #columns = Student.__table__.columns.keys()

        return redirect(url_for('show_table', table_name='Student', page=1))

    return render_template('insert_row_student.html', form=form, action='addStudents')


@app.route('/Tests/insert', methods=['GET', 'POST'])
def addTests():
    form = TestForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('insert_row_test.html', action='addTests', form=form)
        newTest = Test(
            student_id=form.student_id.data,
            yeartest=form.yeartest.data,
            test_name=form.test_name.data,
            lang=form.lang.data,
            subtest=form.subtest.data,
            teststatus=form.teststatus.data,
            ball100=form.ball100.data,
            ball12=form.ball12.data,
            dpalevel=form.dpalevel.data,
            ball=form.ball.data,
            adaptscale=form.adaptscale.data,
            test_loc_id=form.test_loc_id.data
        )
        if dbms == 'postgres':
            db.session.add(newTest)
            db.session.commit()
        redisClient.flushall()

        #new_test = Test.query.filter_by(student_id=newTest.student_id, yeartest=newTest.yeartest,
        #                                test_name=newTest.test_name).first()
        #tests = Test.query.filter(Test.student_id != newTest.student_id, Test.yeartest != newTest.yeartest,
        #                          Test.test_name != newTest.test_name).all()
        #tests.insert(0, new_test)
        #columns = Test.__table__.columns.keys()

        return redirect(url_for('show_table', table_name='Tests', page=1))

    return render_template('insert_row_test.html', form=form, action='addTests')


@app.route('/living_area/insert', methods=['GET', 'POST'])
def addLivingArea():
    form = living_areaForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('insert_row_living_area.html', form=form, action='addLivingArea')
        newLiving_area = Living_area(
            regname=form.regname.data,
            areaname=form.areaname.data,
            tername=form.tername.data,
            regtypename=form.regtypename.data,
            tertypename=form.tertypename.data
        )
        if dbms == 'postgres':
            db.session.add(newLiving_area)
            db.session.commit()

        redisClient.flushall()


        return redirect(url_for('show_table', table_name='living_area', page=1))

    return render_template('insert_row_living_area.html', form=form, action='addLivingArea')


@app.route('/test_location/insert', methods=['GET', 'POST'])
def addTest_loc():
    form = test_locationForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('insert_row_test_loc.html', form=form, action='addTest_loc')
        newTest_loc = Test_loc(
            ptname=form.ptname.data,
            ptregname=form.ptregname.data,
            ptareaname=form.ptareaname.data,
            pttername=form.pttername.data
        )
        if dbms == 'postgres':
            db.session.add(newTest_loc)
            db.session.commit()

        redisClient.flushall()

        #new_test_location = Test_loc.query.filter_by(test_loc_id=newTest_loc.test_loc_id).first()
        #test_locations = Test_loc.query.filter(Test_loc.test_loc_id != newTest_loc.test_loc_id).all()
        #test_locations.append(new_test_location)
        #columns = Test_loc.__table__.columns.keys()

        return redirect(url_for('show_table', table_name='test_location', page=1))

    return render_template('insert_row_test_loc.html', form=form, action='addTest_loc')


@app.route('/Student/delete/<outid>/<yeartest>', methods=['POST'])
def delete_row_student(outid, yeartest):
    # Perform logic to delete the specified row from the table
    # You can retrieve the row ID and handle the deletion
    row = Student.query.filter_by(outid=outid, yeartest=yeartest).first()
    columns = Student.__table__.columns.keys()
    redisClient.flushall()

    if row:
        if Test.query.filter_by(student_id=outid, yeartest=yeartest).first():
#            data = db.session.query(Student)
            error_message = 'Cannot delete the row. It has foreign key references in other tables.'
            flash(error_message)
            show_table(Student)
            return redirect(url_for('show_table', table_name='Student', page=1))

    if dbms == 'postgres':
        if row:
            db.session.delete(row)
            db.session.commit()
        data = db.session.query(Student)

    return redirect(url_for('show_table', table_name='Student', page=1))
            
@app.route('/Tests/delete/<student_id>/<yeartest>/<test_name>', methods=['POST'])
def delete_row_test(student_id, yeartest, test_name):
    row = Test.query.filter_by(student_id=student_id, yeartest=yeartest, test_name=test_name).first()
    print(row)
    columns = Test.__table__.columns.keys()
    redisClient.flushall()
    if dbms == 'postgres':
        if row:
            db.session.delete(row)
            db.session.commit()
        data = db.session.query(Test)

    return redirect(url_for('show_table', table_name='Tests', page=1))

@app.route('/living_area/delete/<living_area_id>', methods=['POST'])
def delete_row_liv(living_area_id):
    row = Living_area.query.get(living_area_id)
    columns = Living_area.__table__.columns.keys()
    redisClient.flushall()

    if row:
        if Student.query.filter_by(living_area_id=living_area_id).first():
            data = db.session.query(Living_area)
            error_message = 'Cannot delete the row. It has foreign key references in other tables.'
            flash(error_message)
            show_table(Living_area)
            return redirect(url_for('show_table', table_name='living_area', page=1))
        
#    if row:
#        db.session.delete(row)
#        db.session.commit()
#    data = db.session.query(Living_area)

    return redirect(url_for('show_table', table_name='living_area', page=1))
            
@app.route('/school/delete/<eo_id>', methods=['POST'])
def delete_row_school(eo_id):
    columns = School.__table__.columns.keys()
    row = School.query.get(eo_id)

    redisClient.flushall()
    if row:
        if Student.query.filter_by(eo_id=eo_id).first():
#            data = db.session.query(School)
            error_message = 'Cannot delete the row. It has foreign key references in other tables.'
            flash(error_message)
            show_table(School)
            return redirect(url_for('show_table', table_name='school', page=1))
    
#    if row:
#        db.session.delete(row)
#        db.session.commit()

#    data = db.session.query(School)
    return redirect(url_for('show_table', table_name='school', page=1))
            
@app.route('/test_location/delete/<test_loc_id>', methods=['POST'])
def delete_row_test_l(test_loc_id):
    row = Test_loc.query.get(test_loc_id)
    columns = Test_loc.__table__.columns.keys()

    redisClient.flushall()
    if row:
        if Test.query.filter_by(test_loc_id=test_loc_id).first():
            print("error")
            data = db.session.query(Test_loc)
            error_message = 'Cannot delete the row. It has foreign key references in other tables.'
            flash(error_message)
            show_table(test_loc_id)
            return redirect(url_for('show_table', table_name='test_location', page=1))

    print("error ignored")
#    if row:
#        db.session.delete(row)
#        db.session.commit()
#    data = db.session.query(Test_loc)

    return redirect(url_for('show_table', table_name='test_location', page=1))


@app.route('/query', methods=['GET', 'POST'])
def showQuery():
    form = QueryForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('query.html', form=form, action='showQuery')

        Regions = form.regname.data
        if 'all' in Regions:
            Regions = [region[0] for region in form.regname.choices[1:]]
        test_name = form.test_name.data
        yeartest = form.yeartest.data

        results, regionsDB = [], []
        for region in Regions:
            cacheKey = f"{region}_{test_name}_{yeartest}"
            ball100 = redisClient.get(cacheKey)
            if ball100 is not None and type(ball100) == int and ball100 > -1:
                results.append({'regname': region, 'ball100': ball100})
            else:
                regionsDB.append(region)

        if len(regionsDB) > 0:
            query = (
                db.session.query(
                    Living_area.regname,
                    Student.yeartest,
                    func.min(Test.ball100).label('ball100')
                )
                .join(Student, Student.living_area_id == Living_area.living_area_id)
                .join(Test, Test.student_id == Student.outid)
                .filter(Test.teststatus == 'Зараховано',
                        Test.test_name == test_name,
                        cast(Test.yeartest, Integer) == yeartest,
                        Living_area.regname.in_(regionsDB))
                .group_by(Living_area.regname, Student.yeartest)
            )
            regionsDB = db.session.execute(query).fetchall()

            for region in regionsDB:
                results.append(region)
                # Caching data
                cacheKey = f"{region.regname}_{test_name}_{yeartest}"
                redisClient.set(cacheKey, float(region.ball100))
                redisClient.expire(cacheKey, CACHELIFETIME)

        results = sorted(results, key=lambda x: x['ball100'] if isinstance(x, dict) else x.ball100,
                         reverse=True)
        return render_template('query.html', statistics=results, form=form)

    return render_template('query.html', statistics=[], form=form, action='showQuery')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
