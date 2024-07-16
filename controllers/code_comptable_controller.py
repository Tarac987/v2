from sqlalchemy.orm import Session
from models.code_comptable import CodeComptable

class CodeComptableController:
    def __init__(self, db: Session):
        self.db = db

    def create_code_comptable(self, code: str, description: str):
        code_comptable = CodeComptable(code=code, description=description)
        self.db.add(code_comptable)
        self.db.commit()
        return code_comptable

    def get_code_comptable(self, code_comptable_id: int):
        return self.db.query(CodeComptable).filter(CodeComptable.id == code_comptable_id).first()

    def update_code_comptable(self, code_comptable_id: int, code: str, description: str):
        code_comptable = self.get_code_comptable(code_comptable_id)
        if code_comptable:
            code_comptable.code = code
            code_comptable.description = description
            self.db.commit()
        return code_comptable

    def delete_code_comptable(self, code_comptable_id: int):
        code_comptable = self.get_code_comptable(code_comptable_id)
        if code_comptable:
            self.db.delete(code_comptable)
            self.db.commit()
        return code_comptable

    def get_code_comptable_by_code(self, code: str):
        return self.db.query(CodeComptable).filter(CodeComptable.code == code).first()

    def get_all_codes_comptables(self):
        return self.db.query(CodeComptable).all()
