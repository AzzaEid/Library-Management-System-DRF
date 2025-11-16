from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.schema import SQLAlchemySchemaOpts
from marshmallow import fields, validate
from models.sqlalchemy_models import Author, Book, Member, MemberBook
from .context.database import Session

class BaseOpts(SQLAlchemySchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = Session
        super(BaseOpts, self).__init__(meta, ordered=ordered)

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta(BaseOpts):
        model = Author
        load_instance = True
        include_relationships = False

class BookSchema(SQLAlchemyAutoSchema):
    author = fields.String(attribute='author.name', dump_only=True)
    author_id = auto_field(dump_only=False, load_only=True)
    
    class Meta(BaseOpts):
        model = Book
        load_instance = True
        include_fk = True
        exclude = ('member_books',)

class MemberSchema(SQLAlchemyAutoSchema):
    user_name = fields.String(attribute='username', dump_only=True)
    username = auto_field(load_only=True)
    password = auto_field(load_only=True)
    joined_date = auto_field(dump_only=True)
    
    class Meta(BaseOpts):
        model = Member
        load_instance = True
        exclude = ('member_books',)

class MemberBookSchema(SQLAlchemyAutoSchema):
    book = fields.Nested(BookSchema, dump_only=True)
    member = fields.Nested(MemberSchema, dump_only=True)
    is_overdue = fields.Boolean(dump_only=True)
    is_returned = fields.Boolean(dump_only=True)
    days_overdue = fields.Integer(dump_only=True)
    
    class Meta(BaseOpts):
        model = MemberBook
        load_instance = True
        include_fk = True

class MemberBookCreateSchema(SQLAlchemyAutoSchema):
    borrow_period_days = fields.Integer(
        load_only=True,
        missing=14,
        validate=validate.Range(min=1, max=30)
    )
    
    class Meta(BaseOpts):
        model = MemberBook
        load_instance = False
        fields = ('book_id', 'member_id', 'borrow_period_days')