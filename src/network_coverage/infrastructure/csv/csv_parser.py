import csv
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage
from src.network_coverage.infrastructure.csv.lambert93_to_gps import lambert93_to_gps
from src.network_coverage.infrastructure.persistence.sqlite.database import SessionLocal


def import_csv(csv_file: str, batch_size: int = 1000, session=None):
    own_session = False
    if session is None:
        session = SessionLocal()
        own_session = True

    batch = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                x = int(row["x"])
                y = int(row["y"])
            except ValueError:
                # Skip invalid coordinates
                continue

            long, lat = lambert93_to_gps(x, y)

            batch.append(NetworkCoverage(
                code=int(row["Operateur"]),
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

    if own_session:
        session.close()
