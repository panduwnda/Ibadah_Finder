from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
from geoalchemy2 import Geometry
from sqlalchemy import func
from forms import TempatIbadahForm  # Import form yang sudah Anda buat
import json


# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'random_secret_key'  # Ganti dengan secret key Anda
app.config['SECRET_KEY'] = 'your_random_secret_key'


# Menetapkan SECRET_KEY untuk perlindungan CSRF
app.config['SECRET_KEY'] = 'your_random_secret_key'

# Inisialisasi SQLAlchemy dan CSRF
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Model untuk data tempat ibadah (Spatial Data)
class SpatialData(db.Model):
    __tablename__ = 'saranaibadah_pt_50k'  # Nama tabel
    gid = db.Column(db.Integer, primary_key=True)  # Primary Key
    namobj = db.Column(db.String(255))  # Nama objek
    luas = db.Column(db.Numeric)  # Luas objek
    remark = db.Column(db.String(255))  # Remark
    geom = db.Column(Geometry('POINT', srid=4326))  # Kolom geometri (titik)

# Model untuk data kecamatan (batas wilayah)
class Kecamatan(db.Model):
    __tablename__ = 'administrasikecamatan_ar_50k'  # Nama tabel
    gid = db.Column(db.Integer, primary_key=True)  # Primary Key
    kdppum = db.Column(db.String(255))
    namobj = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    geom = db.Column(Geometry('POLYGON', srid=4326))  # Geometri untuk batas wilayah

# Route untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html', title="Halaman Utama")

# Route untuk halaman Admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = TempatIbadahForm()  # Inisialisasi form

    if form.validate_on_submit():
        # Mengambil data dari form
        namobj = form.nama.data
        luas = form.luas.data
        remark = form.remark.data
        lat = form.latitude.data
        lon = form.longitude.data

        # Membuat objek SpatialData baru
        new_place = SpatialData(
            namobj=namobj,
            luas=luas,
            remark=remark,
            geom=func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)  # Membuat geometri titik
        )

        # Menyimpan objek ke dalam database
        db.session.add(new_place)
        db.session.commit()

        # Redirect ke halaman admin setelah berhasil menambahkan
        return redirect(url_for('admin'))

    # Mengambil semua tempat ibadah dari database
    places_of_worship = SpatialData.query.all()
    return render_template('admin.html', places_of_worship=places_of_worship, form=form)

# Route untuk tampilan peta
@app.route('/map')
def map_view():
    try:
        # Query data titik tempat ibadah
        points = db.session.query(
            SpatialData.namobj,
            SpatialData.luas,
            SpatialData.remark,
            func.ST_AsGeoJSON(SpatialData.geom).label('geom')
        ).all()

        # Query data kecamatan
        kecamatan_data = db.session.query(
            Kecamatan.namobj,
            Kecamatan.remark,
            func.ST_AsGeoJSON(Kecamatan.geom).label('geom')
        ).all()

        # Membuat FeatureCollection GeoJSON untuk titik
        points_geojson = {
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
            points_geojson['features'].append(feature)

        # Membuat FeatureCollection GeoJSON untuk kecamatan
        kecamatan_geojson = {
            'type': 'FeatureCollection',
            'features': []
        }

        for kecamatan in kecamatan_data:
            feature = {
                'type': 'Feature',
                'geometry': json.loads(kecamatan.geom),  # Konversi geometri ke JSON
                'properties': {
                    'name': kecamatan.namobj,
                    'remark': kecamatan.remark
                }
            }
            kecamatan_geojson['features'].append(feature)

        # Mengirimkan data GeoJSON ke template
        return render_template(
            'map.html',
            points=json.dumps(points_geojson),
            kecamatan=json.dumps(kecamatan_geojson)
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        empty_geojson = {'type': 'FeatureCollection', 'features': []}
        return render_template('map.html', points=json.dumps(empty_geojson), kecamatan=json.dumps(empty_geojson))

# Route untuk halaman Edit Tempat Ibadah
@app.route('/admin/edit/<int:place_id>', methods=['GET', 'POST'])
def edit_place(place_id):
    place = SpatialData.query.get_or_404(place_id)  # Mencari tempat ibadah berdasarkan ID
    
    if request.method == 'POST':
        # Update data tempat ibadah berdasarkan input form
        place.namobj = request.form['namobj']
        place.luas = request.form['luas']
        place.remark = request.form['remark']
        # Update geometri (misalnya, jika Anda ingin memperbarui koordinat)
        place.geom = func.ST_SetSRID(func.ST_MakePoint(request.form['lon'], request.form['lat']), 4326)
        
        # Simpan perubahan ke database
        db.session.commit()
        return redirect(url_for('admin'))  # Redirect kembali ke halaman admin setelah update
    
    # Jika metode GET, kita tampilkan form dengan data tempat ibadah yang sudah ada
    return render_template('edit_place.html', place=place)

# Route untuk menghapus Tempat Ibadah
@app.route('/admin/delete/<int:place_id>', methods=['GET'])
def delete_place(place_id):
    place = SpatialData.query.get_or_404(place_id)  # Mencari tempat ibadah berdasarkan ID
    
    db.session.delete(place)  # Menghapus tempat ibadah dari database
    db.session.commit()  # Simpan perubahan ke database
    
    return redirect(url_for('admin'))  # Redirect kembali ke halaman admin setelah penghapusan

if __name__ == '__main__':
    app.run(debug=True)
