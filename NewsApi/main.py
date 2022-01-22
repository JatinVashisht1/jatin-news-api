from dataclasses import fields
from flask import Flask, Response, request, jsonify
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basedb.db'
db = SQLAlchemy(app)

class NewsModel(db.Model):
    # id= db.Column(db.Integer, primary_key=True),
    # title = db.Column(db.String, nullable = False)
    # news = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    news = db.Column(db.String, nullable=False)
    imageurl = db.Column(db.String)
    # likes = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"News({title}, {news}, {imageurl})"
        # pass
# db.create_all()
    
news_post_arguments = reqparse.RequestParser()
news_post_arguments.add_argument('id', type=int, help='primary key')
news_post_arguments.add_argument('title', type=str, help='title of the news', required=True)
news_post_arguments.add_argument('news', type=str, help='detail of the news')
news_post_arguments.add_argument('imageurl', type=str, help='image url of the news')

news_post_arg = reqparse.RequestParser()
news_post_arg.add_argument('newslist', type = list, help = 'news list', required = True)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'news': fields.String,
    'imageurl': fields.String
}


class NewsApi(Resource):
    @marshal_with(resource_fields)    
    def get(self, news_id=-1):
        # data = NewsModel.query.all()
        if news_id == -1:
            data = NewsModel.query.all()
            if not data:
                abort(http_status_code=404, message='No news available')
            return data
            
        data = NewsModel.query.filter_by(id=news_id).first()
        if not data:
            abort(http_status_code=404, message='news not exist')
        return data
    
    @marshal_with(resource_fields)
    def post(self, news_id):
        args = news_post_arguments.parse_args()
        result = NewsModel.query.filter_by(id=news_id).first()
        if not result:
            news = NewsModel(id=news_id, title=args['title'], news=args['news'], imageurl=args['imageurl'])
            db.session.add(news)
        else:
            result.news = args['news']
            result.title = args['title']
            result.imageurl = args['imageurl']

        db.session.commit()
        return '', 204
    
    def delete(self, news_id):
        result = NewsModel.query.filter_by(id=news_id).first()
        if not result:
            abort(http_status_code=404, message='This news is not available')
        
        
  
api.add_resource(NewsApi, '/news/<int:news_id>', '/news')

if(__name__=='__main__'):
    app.run(debug=True, host="0.0.0.0")