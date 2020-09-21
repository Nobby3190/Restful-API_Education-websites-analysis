import flask
from flask_restful import Api, Resource
from resources.user import Users, User
from resources.accounts import accounts, account
import pymysql
from flask import jsonify
from flask import request

# 產生路由，
app = flask.Flask(__name__)
# 把flask底下的function之下Flask套件之下的網頁帶入app的變數
app.config["DEBUG"] = True
# 設定設定值debug = true
api = Api(app)
# 把app這個網站套上api
api.add_resource(Users,"/users")
# 增加來源-在(Users)user.py裡設定的api方法，/users是網址
api.add_resource(User,"/user/<id>")
# id變數可以被get跟post抓到
api.add_resource(accounts,"/accounts")
api.add_resource(account,"/account/<id>")

@app.route('/',methods = ['GET'])
# 斜線的部分是任意的網址
# 往下執行下面的函數，並用方法get
def home():
    return "<h2>Hello World</h2>"

# @app.route('/cool',methods = ['GET'])

# def cool():
#     return "<h2>So cool</h2>"

# 錯誤包裝
@app.errorhandler(Exception)
# flask偵測到錯誤產生，就去偵測錯誤的程式碼
def handle(error):
    code = 500
    if type(error).__name__ == "NotFound":
        #錯誤名稱是notfound的話，回傳code 404
        code = 404
    return {
        'msg':type(error).__name__
    },code
# 讓出現錯誤時程式碼不要爆漏出來


# 驗證 
@app.before_request
def auth():
    token = request.headers.get('auth')
    # 拿到request裡面的headers，設定金鑰讓取得的人才能進來
    if token == '567':
        pass
    else:
        return {
            'msg':'invalid token',
        },401
    # return兩個變數，dictionart跟status code 401(flask的語法)

@app.route('/account/<account_number>/deposit', methods=['post'])
def deposit(account_number):
    db = pymysql.connect(
        '192.168.56.150',
        'allen',
        'allen0319',
        'test'
    )

    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
    select * from test.Accounts where account_number = {}
    """.format(account_number)
    cursor.execute(sql)
    account = cursor.fetchone()
    money = request.values["money"]
    balance = account['balance'] + int(money)

    sql = """
        UPDATE `test`.`accounts` 
        SET 'balance' = {} 
        WHERE account_number = {};
        """.format(balance, account_number)
    result = cursor.execute(sql)
    db.commit()
    db.close()
    # 給使用api的人回應msg
    response = {"code":200,'msg':"success"}
    if result == 0:
        response['msg'] = 'error'

    return jsonify(response)


    
@app.route('/account/<account_number>/withdraw', methods=['post'])
def withdraw(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] - int(money)
    response = {"code":200, "msg":"success"}
    if balance < 0:
        response['msg'] = 'error'
        response['code'] = 400
        return jsonify(response)
    else:
        sql = """
            UPDATE `test`.`accounts` 
            SET 'balance' = {} 
            WHERE account_number = {};
            """.format(balance, account_number)
        cursor.execute(sql)
        db.commit()
        db.close()
        return jsonify(response)
   
def get_account(account_number):
    db = pymysql.connect(
        '192.168.56.150',
        'allen',
        'allen0319',
        'test'
    )

    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
    select * from test.Accounts where account_number = {}
    """.format(account_number)
    cursor.execute(sql)
    account = cursor.fetchone()
    return db, cursor, account
    # money = request.values["money"]
    # balance = account['balance'] - int(money)
    # response = {"code":200,'msg':"success"}
    # if balance < 0:
    #     response['msg'] = 'error'
    #     response['code'] = 400
    #     sql = """
    #         UPDATE `test`.`accounts` 
    #         SET 'balance' = {} 
    #         WHERE account_number = {};
    #         """.format(balance, account_number)
    #     result = cursor.execute(sql)
    #     db.commit()
    #     db.close()

    # response = {"code":200,'msg':"success"}
    # if result == 0:
    #     response['msg'] = 'error'
    #     response['code'] = 400
    #     return jsonify(response)
    # else:
    #     sql = """
    #         UPDATE `test`.`accounts` 
    #         SET 'balance' = {} 
    #         WHERE account_number = {};
    #         """.format(balance, account_number)
    #     result = cursor.execute(sql)
    #     db.commit()
    #     db.close()
    #     return jsonify(response)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3333)
# 


