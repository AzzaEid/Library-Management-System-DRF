from sqlalchemy import select
from datetime import datetime
from ..models.sqlalchemy_models import AuthToken, Member
from ..context.database import Session

class AuthTokenRepository:
    @staticmethod
    def create_token(member_id):
        session = Session()
        token_str = AuthToken.generate_token()
        token = AuthToken(token=token_str, member_id=member_id)
        session.add(token)
        session.commit()
        session.refresh(token)
        return token
    
    @staticmethod
    def get_by_token(token_str):
        session = Session()
        stmt = select(AuthToken).where(AuthToken.token == token_str)
        token = session.scalar(stmt)
        
        if token and token.expires_at and token.expires_at < datetime.utcnow():
            return None
        
        return token
    
    @staticmethod
    def delete_token(token_str):
        session = Session()
        stmt = select(AuthToken).where(AuthToken.token == token_str)
        token = session.scalar(stmt)
        if token:
            session.delete(token)
            session.commit()
            return True
        return False
    
    @staticmethod
    def delete_member_tokens(member_id):
        session = Session()
        stmt = select(AuthToken).where(AuthToken.member_id == member_id)
        tokens = session.scalars(stmt).all()
        for token in tokens:
            session.delete(token)
        session.commit()