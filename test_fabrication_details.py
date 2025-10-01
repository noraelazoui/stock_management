from models.database import db
from models.fabrication import Fabrication

def test_fabrication_details():
    # Test getting fabrication details
    fabrication_code = "mama"
    fabrication_optim = "1"
    
    print("1. Getting fabrication details...")
    details = Fabrication.get_details_fabrication(fabrication_code, fabrication_optim)
    
    print("\nDetails retrieved:")
    if details:
        for detail in details:
            print(f"- Article: {detail.get('article')}")
            print(f"  Pourcentage: {detail.get('pourcentage')}%")
            print(f"  Quantité à fabriquer: {detail.get('quantite_fabrique')}")
            print(f"  Prix total: {detail.get('prix_total')}")
            print()
    else:
        print("No details found")
    
    print("\n2. Checking fabrication document in MongoDB...")
    fabrication = db.fabrications.find_one({"code": fabrication_code, "optim": fabrication_optim})
    if fabrication:
        print("Fabrication found:")
        print(f"- Code: {fabrication.get('code')}")
        print(f"- Optim: {fabrication.get('optim')}")
        print(f"- Quantité à fabriquer: {fabrication.get('quantite_a_fabriquer')}")
        print("\nDetail fabrication:")
        detail_fab = fabrication.get('detail-fabrication', {})
        if detail_fab:
            articles = detail_fab.get('article', [])
            for article in articles:
                print(f"- Article: {article.get('article')}")
                print(f"  Pourcentage: {article.get('pourcentage')}%")
                print(f"  Quantité à fabriquer: {article.get('quantite_fabrique')}")
                print(f"  Prix total: {article.get('prix_total')}")
                print()
    else:
        print("Fabrication not found")

if __name__ == "__main__":
    test_fabrication_details()
