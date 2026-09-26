import os
from sqlalchemy.orm import Session
from backend.db.database import engine, Base
from backend.db.models import Contributor, TrustedKey
from backend.core.crypto.signing import generate_key_pair
import argparse

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def register_demo_key():
    with Session(engine) as session:
        # Check if already exists
        if session.query(Contributor).filter_by(id="demo_contributor").first():
            print("Demo contributor already exists.")
            return

        contributor = Contributor(id="demo_contributor", name="Demo Contributor")
        session.add(contributor)
        
        priv, pub = generate_key_pair()
        
        key = TrustedKey(
            contributor_id="demo_contributor",
            public_key=pub.decode('utf-8'),
            fingerprint="demo_fingerprint_001"
        )
        session.add(key)
        session.commit()
        
        # Save keys for testing
        os.makedirs("trusted_keys", exist_ok=True)
        with open("trusted_keys/demo_private.pem", "wb") as f:
            f.write(priv)
        with open("trusted_keys/demo_public.pem", "wb") as f:
            f.write(pub)
            
        print("Demo contributor and keys generated in 'trusted_keys' directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--register", action="store_true")
    args = parser.parse_args()
    
    if args.init:
        init_db()
    if args.register:
        register_demo_key()
