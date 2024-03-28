from flask import Flask, render_template


from models import db, Submit


app = Flask(__name__, static_folder='./template/static', template_folder='./template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def hello_world():
    return render_template('index.html', ranking=Submit.query.all())

# <form action="/upload" method="post" enctype="multipart/form-data">
@app.route('/upload', methods=['POST'])
def upload():
    return render_template('upload.html', name='World', result='Success')


if __name__ == '__main__':
    app.run(debug=True, port=5001,host='0.0.0.0')


