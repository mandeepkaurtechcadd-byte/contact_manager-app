from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///contact.db"
db = SQLAlchemy(app)

class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(100),nullable=False)
with app.app_context():
    db.create_all() 


@app.route('/',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        
        contact=Contact(name=request.form['name'],
        phone=request.form['phone'],
        email=request.form['email'])
        db.session.add(contact)
        db.session.commit()      
    contacts=Contact.query.all()
   
    search_name=request.args.get('keyword')
   
    if search_name:
        contacts=Contact.query.filter_by(name=search_name).all()
    else:
        contacts=Contact.query.all()
    count=len(contacts)       
    return render_template('contact.html',contacts=contacts,count=count)

@app.route("/edit_contact/<int:id>",methods=['GET','POST'])
def edit_contact(id):
    contact=Contact.query.get(id)
    if request.method=="POST":
        contact.name=request.form.get('name')
        contact.phone=request.form.get('phone')
        contact.email=request.form.get('email')
        db.session.commit()
        return redirect(url_for('contact'))
    return render_template('edit_contact.html',contact=contact)

@app.route("/delete_contact/<int:id>")
def delete_contact(id):
    contact=Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('contact'))
        
if __name__=="__main__":
    app.run(debug=True)