import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base, NetworkCoverage
from src.network_coverage.infrastructure.csv.lambert93_to_gps import lambert93_to_gps


def create_session(db_file: str = ":memory:"):
    engine = create_engine(f"sqlite:///{db_file}", future=True)
    with engine.connect() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def import_csv(csv_file: str, db_file: str = "coverage.db", batch_size: int = 1000, session=None):
    if session is None:
        session = create_session(db_file)

    batch = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            long, lat = lambert93_to_gps(int(row["x"]), int(row["y"]))

            batch.append(NetworkCoverage(
                operateur=int(row["Operateur"]),
                long=long,
                lat=lat,
                g2=bool(int(row["2G"])),
                g3=bool(int(row["3G"])),
                g4=bool(int(row["4G"]))
            ))

            if len(batch) >= batch_size:
                session.add_all(batch)
                session.commit()
                batch.clear()

    if batch:
        session.add_all(batch)
        session.commit()

    session.close()

if __name__ == "__main__":
    import_csv("data.csv")
