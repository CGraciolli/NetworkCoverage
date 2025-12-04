import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base, NetworkCoverage
from src.network_coverage.infrastructure.csv.lamber93_to_gps import lamber93_to_gps

def import_csv(csv_file: str, db_file: str = "coverage.db", batch_size: int = 1000):
    engine = create_engine(f"sqlite:///{db_file}", echo=True, future=True)

    # Enable foreign keys (optional, good practice)
    with engine.connect() as conn:
        conn.execute("PRAGMA foreign_keys = ON")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    batch = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            long, lat = lamber93_to_gps(int(row["x"]), int(row["y"]))

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
