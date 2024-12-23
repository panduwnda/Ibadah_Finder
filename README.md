# Sistem Informasi Pariwisata Lampung (SIPALUNG)

| Nama                  | NIM       |
| --------------------  | --------- |
| Bani Adam Tampubolon  | 121140187 |
| Zahra Areefa Ananta   | 121140138 |
| Pandu Putra Mulwanda  | 121140    |
| Dila Ayu Prastita     | 121140    |
| Varell Anthonio       | 121140    |

## Deskripsi Proyek

Ibadah Finder" adalah sebuah sistem informasi geografis berbasis web yang dirancang untuk membantu masyarakat menemukan tempat ibadah di wilayah Bandar Lampung. Sistem ini menyediakan informasi lokasi masjid, gereja, pura, wihara, dan tempat ibadah lainnya dengan fitur pemetaan interaktif. Dengan memanfaatkan teknologi pemetaan modern, pengguna dapat dengan mudah mencari dan menavigasi lokasi tempat ibadah yang mereka butuhkan.

## Fitur Utama

1. **Peta Interaktif & Routing**

    - Peta dinamis dengan berbagai layer (OpenStreetMap, Satellite, Topographic)
    - Navigasi, penentuan rute, serta estimasi jarak dan waktu tempuh
    - Tampilan color marker yang berbeda untuk setiap kategori tempat ibadah

2. **Manajemen Data Wisata**

    - Penambahan titik tempat ibadah
    - Pembentukan area wilayah per kecamatan dengan polygon
    - Pencarian tempat ibadah dalam menu admin
    

3. **Filter & Kategori**
    - Pencarian lokasi ibadah dengan fitur filter
    - Filter kategori (misal Masjid, Gereja, Pura, Vihara, dll.)
    - Daftar tempat ibadah terorganisir untuk memudahkan eksplorasi

4. **Analisis Data Spasial**
    - Menampilkan analisis jarak, jumlah tempat ibadah

## Teknologi yang Digunakan

-   **Frontend**: HTML, CSS, JavaScript
-   **Backend**: Python (Flask)
-   **Database**: PostgreSQL dengan ekstensi PostGIS
-   **Map Library**: Leaflet.js
-   **Routing**: Leaflet Routing Machine

## Struktur Proyek

```
IBADAH_FINDER/
├── static/
│   ├── css/
│   │   └── style.css
|   |   └── admin.css
│   ├── js/
│   │   ├── script.js
│   └── images/
├── templates/
│   └── index.html
│   └── admin.html
│   └── base.html
│   └── edit_place.html
│   └── map.html
│   └── profile.html
├── app.py
├── config.py
├── forms.py
├── requirement.txt
└── README.md
```

## Instalasi dan Penggunaan

1. Clone repository ini
2. Install dependencies Python:
    ```bash
    pip install -r requirements.txt
    ```
3. Siapkan database PostgreSQL dengan PostGIS
4. Sesuaikan konfigurasi database di `config.py`
5. Jalankan aplikasi:
    ```bash
    python app.py
    ```

## Panduan Penggunaan

1. Pastikan semua dependensi (Flask, psycopg2, dll.) sudah diinstal.
2. Jalankan server dengan perintah:
    ```
    python app.py
    ```
3. Buka browser pada alamat http://127.0.0.1:5000
4. Gunakan sidebar untuk mencari dan memfilter lokasi wisata.
5. Klik "Menu Admin", "Tambah Titik", ataupun "Hapus Data" untuk mengupdate data sarana tempat ibadah.
