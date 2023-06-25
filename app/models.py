from main import db

class Living_area(db.Model):
    tablename = 'living_area'

    living_area_id = db.Column(db.Integer, primary_key=True)
    regname = db.Column(db.String(80), nullable=False)
    areaname = db.Column(db.String(80), nullable=False)
    tername = db.Column(db.String(80), nullable=False)
    regtypename = db.Column(db.String(80), nullable=False)
    tertypename = db.Column(db.String(80), nullable=False)

    living_area = db.relationship("Student", backref="Living_area", lazy=True, cascade="all, delete-orphan")

class School(db.Model):
    tablename = 'school'

    eo_id = db.Column(db.Integer, primary_key=True)
    eoname = db.Column(db.String(400), nullable=False)
    eotypename = db.Column(db.String(250), nullable=False)
    eoregname = db.Column(db.String(250), nullable=False)
    eoareaname = db.Column(db.String(250), nullable=False)
    eotername = db.Column(db.String(250), nullable=False)
    eoparent = db.Column(db.String(250), nullable=False)

    students = db.relationship("Student", backref = 'School', lazy=True, cascade="all, delete-orphan")

class Student(db.Model):
    tablename = 'student'

    outid = db.Column(db.String(40), primary_key=True)
    yeartest = db.Column(db.Integer, nullable=False)
    birth = db.Column(db.Integer, nullable=False)
    sextypename = db.Column(db.String(20), nullable=False)
    classprofilename = db.Column(db.String(120), nullable=False)
    classlangname = db.Column(db.String(40))
    living_area_id = db.Column(db.Integer, db.ForeignKey('living_area.living_area_id'))
    eo_id = db.Column(db.Integer, db.ForeignKey('school.eo_id'))

    tests = db.relationship("Test", backref="Student", lazy=True, cascade="all, delete-orphan")

    # SQL: CONSTRAINT student_id PRIMARY KEY (OUTID, YearTest)
    table_args = (
        db.PrimaryKeyConstraint('outid', 'yeartest', name='student_id'),
    )


class Test(db.Model):
    tablename = 'test'

    student_id = db.Column(db.String(36), db.ForeignKey('student.outid'), primary_key=True)
    yeartest = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(60), primary_key=True)
    lang = db.Column(db.String(10))
    subtest = db.Column(db.String(120))
    teststatus = db.Column(db.String(60))
    ball100 = db.Column(db.Float)
    ball12 = db.Column(db.Float)
    dpalevel = db.Column(db.String(40))
    ball = db.Column(db.Float)
    adaptscale = db.Column(db.String(40))
    test_loc_id = db.Column(db.Integer, db.ForeignKey('test_loc.test_loc_id'))

    table_args = (
        db.PrimaryKeyConstraint('student_id', 'yeartest', 'test_name', name='test_id'),
    )


class Test_loc (db.Model):
    tablename = 'test_loc'

    test_loc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptname = db.Column(db.String(120))
    ptregname = db.Column(db.String(120))
    ptareaname = db.Column(db.String(120))
    pttername = db.Column(db.String(120))

    tests = db.relationship("Test", backref = 'Test_loc', lazy=True, cascade="all, delete-orphan")
