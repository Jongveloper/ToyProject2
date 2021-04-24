from flask import Flask, render_template, request, redirect, url_for, session

class User:
   def __init__(self, id, username, password):
      self.id = id
      self.username = username
      self.password = password

   def __repr__(self):
      return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='woo', password='1234'))
users.append(User(id=2, username='chilsung', password='1234'))



app = Flask(__name__)
app.secret_key = 'qlasldldldldldlf'

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      session.pop('user_id', None)

      username = request.form['username']
      password = request.form['password']

      user = [x for x in users if x.username == username][0]
      if user and user.password == password:
         session['user_id'] =user.id
         return redirect(url_for('main'))

      return redirect(url_for('login'))

   return render_template('login.html')
@app.route('/main')
def main():
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

