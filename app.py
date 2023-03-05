# flask 준비
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# pymongo 준비
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.6h3ijoc.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# 본문

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def mars_post():
    # 프론트 택배원이 가져온 택배(사용자가 넣은 정보) 받기
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give'] 
    
    # DB에 넣기 (pymongo)
    userBuy = {
        'name':name_receive,
        'address':address_receive,
        'size':size_receive
        }
    db.mars.insert_one(userBuy)

    # POST로 DB에 넣었으니 '저장 완료' 리턴 -> 프론트에서 창 띄우기 
    return jsonify({'msg':'저장 완료'})

@app.route("/mars", methods=["GET"])
def mars_get():
    # DB에서 모든 데이터 다 갖고오기 -> 클라이언트에 내려주기.
    marsData = list(db.mars.find({},{'_id':False}))
    return jsonify({'result':marsData})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)