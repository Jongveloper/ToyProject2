from flask import Flask, render_template, request, redirect, url_for, session, jsonify

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

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
client = MongoClient('localhost', 27017)
db = client.dbsparta

app.secret_key = 'qlasldldldldldlf'

@app.route('/', methods=['GET', 'POST'])
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

# HTML 주는 부분
@app.route('/movie')
def movie():
   return render_template('movie.html')

@app.route('/memo', methods=['GET'])
def listing():
   articles = list(db.articles.find({}, {'_id': False}))
   return jsonify({'all_articles': articles})

# API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
   url_receive = request.form['url_give']
   comment_receive = request.form['comment_give']

   url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=171539'

   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_receive, headers=headers)

   soup = BeautifulSoup(data.text, 'html.parser')

   title = soup.select_one('meta[property="og:title"]')['content']
   image = soup.select_one('meta[property="og:image"]')['content']
   desc = soup.select_one('meta[property="og:description"]')['content']

   doc = {
      'title': title,
      'image': image,
      'desc': desc,
      'url': url_receive,
      'comment': comment_receive
   }

   db.articles.insert_one(doc)

   return jsonify({'msg': '좋은 영화 공유해주셔서 감사합니다!'})

@app.route('/event')
def event():
   return render_template('event.html')

# 주문하기(POST) API
@app.route('/comm', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']


    doc = {
        'name': name_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.comm.insert_one(doc)

    return jsonify({'msg': '응모완료!'})

# 주문 목록보기(Read) API
@app.route('/comm', methods=['GET'])
def view_orders():
    event = list(db.comm.find({}, {'_id': False}))
    return jsonify({'comm': event})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

