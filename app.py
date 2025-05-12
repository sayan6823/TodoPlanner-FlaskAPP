from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone  
# Cuz utcnow is depreciated

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

app.app_context().push()
class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200),nullable=False )
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default= datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.sno} - {self.title}" 


@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']

        # title=print(request.form['title'])
        # desc=print(request.form['desc'])

        todo = Todo(title=title, desc= desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/") 
    allTodo= Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

    # print(addTodo)
    # return "<p>Hello, World!</p>"

@app.route("/show")
def products():
    # addTodo= Todo.query.all()
    # print(addTodo)
    return "<h2>This is products page</h2>"

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        updateTodo= Todo.query.filter_by(sno=sno).first()
        updateTodo.title=title
        updateTodo.desc=desc
        db.session.add(updateTodo)
        db.session.commit()
        return redirect("/")

    updateTodo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',updateTodo=updateTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    deleteTodo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(deleteTodo)
    db.session.commit()
    # print(addTodo)
    return redirect("/") 

if __name__=="__main__":
    app.debug=True
    app.run()
    app.run(debug=True)
    # app.run(debug=True,host=8000)