from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Tambahkan impor ini
from config import Config
import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class SpatialData(db.Model):
    __tablename__ = 'saranaibadah_pt_50k'  # Nama tabel
    gid = db.Column(db.Integer, primary_key=True)  # Primary Key
    namobj = db.Column(db.String(255))  # Kolom nama objek
    luas = db.Column(db.Numeric)  # Kolom luas
    remark = db.Column(db.String(255))  # Kolom remark
    geom = db.Column(Geometry('POINT', srid=4326))  # Kolom geometri (titik)

@app.route('/')
def home():
    return render_template('index.html', title="Halaman Utama")

@app.route('/map')
def index():
    try:
        # Query semua titik dan konversi ke GeoJSON
        points = db.session.query(
            SpatialData.namobj,
            SpatialData.luas,
            SpatialData.remark,
            func.ST_AsGeoJSON(SpatialData.geom).label('geom')
        ).all()

        # Membuat FeatureCollection GeoJSON
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }

        for point in points:
            feature = {
                'type': 'Feature',
                'geometry': json.loads(point.geom),  # Konversi geometri ke JSON
                'properties': {
                    'name': point.namobj,
                    'luas': str(point.luas),
                    'remark': point.remark
                }
            }
            geojson['features'].append(feature)

        return render_template('map.html', points=json.dumps(geojson))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('map.html', points=json.dumps({'type': 'FeatureCollection', 'features': []}))

if __name__ == '__main__':
    app.run(debug=True)
