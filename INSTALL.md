# GitHub profile — portfolio design edition

## Pasang

1. Buka repository publik ihsanwahyudin/ihsanwahyudin.
2. Ganti README.md dan seluruh folder assets/ dengan isi paket ini. Commit perubahan.
3. Buka profil GitHub. Banner animasi tetap memakai path assets/hero.svg.

## Desain yang disamakan

Acuan: src/components/sections/Hero.tsx, src/styles/globals.css, src/components/ui/CodeMark.tsx dan src/data/portfolio.ts dari /Users/ihsan/Repository/portofolio-web, 19 Oktober 2026.

- Font Geist dan Geist Mono; outline vektor menjaga bentuk huruf tanpa unduhan font saat profil dibuka.
- Warna persis: canvas #f3f2ee, ink #111113, accent #5b4cf5, lavender #ded8ff, mint #cdeedd, peach #ffdcc7, sky #d3e7ff.
- Hero memakai dua kartu pilihan: perkenalan dan tech stack. Keduanya selebar profil, dengan radius 28 dan marquee dua arah.
- Logo dan screenshot proyek asli dari folder public/ website; tidak memakai screenshot atau data contoh buatan.
- Gradasi bergerak, glow lavender/peach, dan marquee CSS dua arah; menghormati prefers-reduced-motion.
- Tidak bergantung pada server gambar untuk aset desain. Semua gambar yang ditampilkan disimpan dalam repository.

## Batas tampilan GitHub

SVG di README adalah gambar. Kontrol di dalam banner merupakan bagian gambar, bukan tombol HTML terpisah. Seluruh banner membuka portfolio; tiga kartu kontak di bawah banner memiliki tautan masing-masing. Hover 3D, navigasi scroll, dan jam lokal real-time website tidak berjalan di gambar GitHub. Hero hanya memuat perkenalan dan tech stack. Logo SVG mempertahankan atribut fill dan stroke asli. Ikon kode memakai tiga path terpisah seperti CodeMark.tsx.

hero-static.svg menyediakan versi tanpa animasi. Untuk memakainya, ubah src banner pada README menjadi ./assets/hero-static.svg.

## Kredit

Font: Geist / Geist Mono (SIL Open Font License), https://github.com/google/fonts/tree/main/ofl/geist dan https://github.com/google/fonts/tree/main/ofl/geistmono. Lisensi disertakan di folder licenses/.
CodeMark dan ikon antarmuka diadaptasi dari komponen website. Lucide code-xml memakai lisensi ISC.
