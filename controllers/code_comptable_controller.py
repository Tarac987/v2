# controllers/code_comptable_controller.py
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

    def initialize_codes_comptables(self):
        codes = [
            {"code": "101", "description": "Capital"},
            {"code": "102", "description": "Primes d'émission, de fusion, d'apport"},
            {"code": "103", "description": "Réserves"},
            {"code": "104", "description": "Report à nouveau"},
            {"code": "105", "description": "Subventions d'investissement"},
            {"code": "106", "description": "Provisions réglementées"},
            {"code": "201", "description": "Immobilisations incorporelles"},
            {"code": "202", "description": "Immobilisations corporelles"},
            {"code": "203", "description": "Immobilisations en cours"},
            {"code": "204", "description": "Amortissements des immobilisations incorporelles"},
            {"code": "205", "description": "Amortissements des immobilisations corporelles"},
            {"code": "301", "description": "Stocks de matières premières"},
            {"code": "302", "description": "Stocks de produits en cours"},
            {"code": "303", "description": "Stocks de produits finis"},
            {"code": "304", "description": "Stocks de marchandises"},
            {"code": "401", "description": "Fournisseurs et comptes rattachés"},
            {"code": "402", "description": "Fournisseurs d'immobilisations"},
            {"code": "403", "description": "Clients et comptes rattachés"},
            {"code": "404", "description": "Autres créances"},
            {"code": "405", "description": "Autres dettes"},
            {"code": "501", "description": "Banque"},
            {"code": "502", "description": "Caisse"},
            {"code": "503", "description": "Placements à court terme"},
            {"code": "504", "description": "Emprunts et dettes financières à moyen et long terme"},
            {"code": "601", "description": "Achats de matières premières"},
            {"code": "602", "description": "Achats de marchandises"},
            {"code": "603", "description": "Charges externes"},
            {"code": "604", "description": "Impôts, taxes et versements assimilés"},
            {"code": "605", "description": "Charges de personnel"},
            {"code": "606", "description": "Dotations aux amortissements"},
            {"code": "701", "description": "Ventes de produits finis"},
            {"code": "702", "description": "Ventes de marchandises"},
            {"code": "703", "description": "Subventions d'exploitation"},
            {"code": "704", "description": "Autres produits"},
            {"code": "801", "description": "Comptes de régularisation"},
            {"code": "802", "description": "Comptes d'ajustements"},
            {"code": "803", "description": "Comptes de provisions pour risques et charges"}
        ]

        for code in codes:
            if not self.get_code_comptable_by_code(code["code"]):
                self.create_code_comptable(code["code"], code["description"])
