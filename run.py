from flask import Flask, request, jsonify, make_response
from flask_restplus import Resource, Api, fields, reqparse
from models.modles import Book,db
from flask_cors import CORS
import platform
sql_url = ""
if(platform.system() =="Windows"):
    sql_url = 'sqlite:///F:/Python/fla02/test3.db'
elif(platform.system() =="Linux"):
    sql_url = 'sqlite:////home/fla02/test3.db'

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            )
CORS(app,resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True     #开启事务
app.config['SQLALCHEMY_DATABASE_URI'] =  sql_url   #连接地址
db.init_app(app)
api = Api(app, version='1.0', title='书籍管理 API',
    description='书籍管理',
)
# 下方显示的增加的参数
mode0 = api.model('查询的参数',{
    'id':fields.Integer(required=True,description="The todo ID"),
    'title':fields.String(required=True,description="The todo ID"),
    'auther':fields.String(required=True,description="The todo ID"),
})
model = api.model('增加的参数',{
    'title':fields.String(required=True,description="The todo ID"),
    'auther':fields.String(required=True,description="The todo ID"),
})
model2 = api.model('删除的参数',{
    'id':fields.Integer(required=True,description="The todo ID"),
    'state':fields.Integer(required=True,description="The todo ID"),
})
model3 = api.model('修改的参数',{
    'id':fields.Integer(required=True,description="The todo ID"),
    'title':fields.String(required=True,description="The todo ID"),
    'auther':fields.String(required=True,description="The todo ID"),
})
ns = api.namespace('api', description='书的操作') #命名空间，相当于Django的父亲路由
#声明全局参数
# parser = reqparse.RequestParser()
# parser.add_argument('title',type=str,help="title")
# parser.add_argument('auther',type=str,help="auther")
def req_result(req):
    resp = make_response(req)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp
@ns.route("/book")  #子路由
class BookList(Resource):
    # 查询操作
    @api.expect(mode0)
    def get(self):
        args = request.args
        # args = request.get_json()
        print(args)

        if args['title'] and args['auther']:
            books = Book.query.filter(Book.title.contains(args['title'])).filter(Book.auther.contains(args['auther']))
        elif args['auther']:
            books = Book.query.filter(Book.auther.contains(args['auther']))
        elif args['title']:
            books = Book.query.filter(Book.title.contains(args['title']))
        elif args['id']:
            books = Book.query.filter(Book.id == args['id'])
        else:
            books = Book.query.all()
        list_books = []
        for b in books:
            collections = {}
            collections['book_id'] = b.id
            collections['book_name'] = b.title
            collections['book_auther'] = b.auther
            list_books.append(collections)
        return req_result(jsonify({'data': 'query sucessful！','result':list_books})) # JsonResponse
    # 添加操作
    @api.expect(model)
    def post(self): #增加一条数据
        # args = parser.parse_args()#获取全部参数
        args = request.get_json()
        print(args)
        book1 = Book(title=args['title'], auther=args['auther'])
        print(book1)
        db.session.add(book1)
        db.session.commit()
        req_result("插入成功")
        return req_result(jsonify({'data':'insert sucessful！'})) #JsonResponse
    # 删除操作
    @api.expect(model2)
    def delete(self):  # 增加一条数据
        # args = parser.parse_args()#获取全部参数
        args = request.get_json()
        # print(args["id"],type(args))
        print(args["state"])
        if args["state"] == 1:
            book1_del = Book.query.filter(Book.id == args["id"]).first()
            # print(book1_del)
            db.session.delete(book1_del)
            db.session.commit()
            req_result("删除成功")
            return req_result(jsonify({'data': 'delete sucessful！'}))  # JsonResponse
        elif args["state"] == 2:
            ids = args["id"].split("-")
            print(ids)
            for id in ids[0:-1]:
                book1_del = Book.query.filter(Book.id == int(id)).first()
                print(book1_del)
                db.session.delete(book1_del)
                db.session.commit()
            return req_result(jsonify({'data': 'delete sucessful！'})) # JsonResponse
    # 修改操作
    @api.expect(model3)
    def put(self):
        args = request.get_json()
        book = Book.query.get(args['id'])
        if book:
            book.title = args['title']
            book.auther = args['auther']
            db.session.add(book)
            db.session.commit()
            return req_result(jsonify({'data':'put sucessful！'}))
        else:
            return req_result(jsonify({'data': 'data is none'}))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get',methods=['GET','POST'])
def hello_get():
    frist = request.args["frist_name"]
    # print(frist + "111111")
    return frist

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9090,debug=True)
