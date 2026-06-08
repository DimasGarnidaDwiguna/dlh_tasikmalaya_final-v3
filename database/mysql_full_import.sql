-- Jalankan file ini lebih dulu di phpMyAdmin atau MySQL CLI.
CREATE DATABASE IF NOT EXISTS dlh_tasikmalaya
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE dlh_tasikmalaya;

-- MySQL schema for DLH Tasikmalaya Flask CMS
-- Import this file first in phpMyAdmin.

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS visitor_logs;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS gallery;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS agenda;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS news_categories;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(140) NOT NULL,
  username VARCHAR(80) NOT NULL UNIQUE,
  email VARCHAR(160) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(40) DEFAULT 'admin',
  is_active_user BOOLEAN DEFAULT TRUE,
  last_login DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  slug VARCHAR(160) NOT NULL UNIQUE,
  icon VARCHAR(30) DEFAULT '🌿',
  summary VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX ix_services_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE news_categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  slug VARCHAR(120) NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE news (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(220) NOT NULL,
  slug VARCHAR(180) NOT NULL UNIQUE,
  excerpt VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  image VARCHAR(255) DEFAULT 'news-1.svg',
  category_id INT NULL,
  author VARCHAR(120) DEFAULT 'Admin DLH',
  views INT DEFAULT 0,
  is_published BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX ix_news_slug (slug),
  CONSTRAINT fk_news_category FOREIGN KEY (category_id) REFERENCES news_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE agenda (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(220) NOT NULL,
  date VARCHAR(20) NOT NULL,
  location VARCHAR(220) NOT NULL,
  description TEXT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(220) NOT NULL,
  category VARCHAR(100) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  year INT NOT NULL,
  description VARCHAR(255) NULL,
  downloads INT DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE gallery (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  image VARCHAR(255) NOT NULL,
  type VARCHAR(20) DEFAULT 'foto',
  video_url VARCHAR(255) NULL,
  album VARCHAR(120) DEFAULT 'Umum',
  description VARCHAR(255) NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE links (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(180) NOT NULL,
  url VARCHAR(255) NOT NULL,
  description VARCHAR(255) NULL,
  icon VARCHAR(30) DEFAULT '🔗',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE contacts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(140) NOT NULL,
  email VARCHAR(160) NOT NULL,
  subject VARCHAR(180) NOT NULL,
  message TEXT NOT NULL,
  status VARCHAR(40) DEFAULT 'Baru',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE complaints (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticket_number VARCHAR(40) UNIQUE,
  name VARCHAR(140) NOT NULL,
  email VARCHAR(160) NOT NULL,
  phone VARCHAR(40) NULL,
  category VARCHAR(80) NOT NULL,
  location VARCHAR(220) NOT NULL,
  message TEXT NOT NULL,
  status VARCHAR(40) DEFAULT 'Masuk',
  admin_response TEXT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX ix_complaints_ticket_number (ticket_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE visitor_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  path VARCHAR(255) NULL,
  ip_address VARCHAR(80) NULL,
  user_agent VARCHAR(255) NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;


-- DATA
-- MySQL seed data converted from the uploaded SQLite database.
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM `visitor_logs`;
DELETE FROM `complaints`;
DELETE FROM `contacts`;
DELETE FROM `links`;
DELETE FROM `gallery`;
DELETE FROM `documents`;
DELETE FROM `agenda`;
DELETE FROM `news`;
DELETE FROM `news_categories`;
DELETE FROM `services`;
DELETE FROM `users`;
ALTER TABLE `users` AUTO_INCREMENT = 1;
INSERT INTO `users` (`id`, `name`, `username`, `email`, `password_hash`, `role`, `is_active_user`, `last_login`, `created_at`) VALUES (1, 'Administrator DLH', 'admin', 'admin@dlh.local', 'pbkdf2:sha256:600000$DLHAdminSeed$664331ab3919f6adc61c58da5252845f2d7fe1cad43087bb52fd4103c4219fcf', 'superadmin', 1, NULL, '2026-06-03 07:08:58.782288');
ALTER TABLE `users` AUTO_INCREMENT = 2;
ALTER TABLE `services` AUTO_INCREMENT = 1;
INSERT INTO `services` (`id`, `title`, `slug`, `icon`, `summary`, `content`, `is_active`, `created_at`, `updated_at`) VALUES (1, 'Perizinan AMDAL', 'amdal', '📑', 'Analisis dampak lingkungan untuk kegiatan berdampak penting.', 'AMDAL merupakan kajian dampak penting suatu usaha atau kegiatan terhadap lingkungan hidup. Layanan ini membantu pemohon memahami alur, persyaratan, dan tahapan persetujuan lingkungan.', 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `services` (`id`, `title`, `slug`, `icon`, `summary`, `content`, `is_active`, `created_at`, `updated_at`) VALUES (2, 'Perizinan IPLC', 'iplc', '💧', 'Pengendalian pembuangan air limbah cair.', 'IPLC berfokus pada pengendalian pembuangan air limbah cair agar memenuhi ketentuan teknis dan baku mutu lingkungan.', 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `services` (`id`, `title`, `slug`, `icon`, `summary`, `content`, `is_active`, `created_at`, `updated_at`) VALUES (3, 'Perizinan SPPL', 'sppl', '✅', 'Surat pernyataan kesanggupan pengelolaan lingkungan.', 'SPPL digunakan untuk usaha atau kegiatan yang tidak wajib AMDAL atau UKL-UPL, tetapi tetap memerlukan komitmen pengelolaan lingkungan.', 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `services` (`id`, `title`, `slug`, `icon`, `summary`, `content`, `is_active`, `created_at`, `updated_at`) VALUES (4, 'Perizinan UKL-UPL', 'ukl-upl', '🌱', 'Dokumen pengelolaan dan pemantauan lingkungan.', 'UKL-UPL berisi rencana pengelolaan dan pemantauan lingkungan untuk kegiatan yang tidak wajib AMDAL, tetapi tetap memiliki dampak lingkungan.', 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `services` AUTO_INCREMENT = 5;
ALTER TABLE `news_categories` AUTO_INCREMENT = 1;
INSERT INTO `news_categories` (`id`, `name`, `slug`, `created_at`, `updated_at`) VALUES (1, 'Berita', 'berita', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `news_categories` (`id`, `name`, `slug`, `created_at`, `updated_at`) VALUES (2, 'Artikel', 'artikel', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `news_categories` (`id`, `name`, `slug`, `created_at`, `updated_at`) VALUES (3, 'Kegiatan', 'kegiatan', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `news_categories` AUTO_INCREMENT = 4;
ALTER TABLE `news` AUTO_INCREMENT = 1;
INSERT INTO `news` (`id`, `title`, `slug`, `excerpt`, `content`, `image`, `category_id`, `author`, `views`, `is_published`, `created_at`, `updated_at`) VALUES (1, 'DLH Kota Tasikmalaya Gelar Aksi Bersih Sungai', 'aksi-bersih-sungai', 'Kolaborasi DLH dan masyarakat dalam menjaga kebersihan sungai.', 'Kegiatan bersih sungai dilakukan untuk meningkatkan kepedulian warga terhadap kebersihan aliran sungai dan pencegahan pencemaran.', 'news-1.svg', 1, 'Admin DLH', 0, 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `news` (`id`, `title`, `slug`, `excerpt`, `content`, `image`, `category_id`, `author`, `views`, `is_published`, `created_at`, `updated_at`) VALUES (2, 'Sosialisasi Pengelolaan Sampah Rumah Tangga', 'sosialisasi-sampah-rumah-tangga', 'Edukasi pemilahan sampah dari sumber.', 'DLH mendorong pemilahan sampah dari rumah sebagai dasar pengelolaan sampah yang lebih efektif dan berkelanjutan.', 'news-2.svg', 2, 'Admin DLH', 0, 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `news` (`id`, `title`, `slug`, `excerpt`, `content`, `image`, `category_id`, `author`, `views`, `is_published`, `created_at`, `updated_at`) VALUES (3, 'Penanaman Pohon Kawasan Perkotaan', 'penanaman-pohon-perkotaan', 'Gerakan penghijauan untuk kualitas udara.', 'Program penanaman pohon dilakukan untuk mendukung kualitas udara, ruang hijau, dan kenyamanan kawasan perkotaan.', 'news-3.svg', 3, 'Admin DLH', 0, 1, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `news` AUTO_INCREMENT = 4;
ALTER TABLE `agenda` AUTO_INCREMENT = 1;
INSERT INTO `agenda` (`id`, `title`, `date`, `location`, `description`, `created_at`, `updated_at`) VALUES (1, 'Sosialisasi Pengelolaan Sampah Rumah Tangga', '2026-06-10', 'Aula DLH Kota Tasikmalaya', 'Edukasi pemilahan dan pengurangan sampah dari rumah.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `agenda` (`id`, `title`, `date`, `location`, `description`, `created_at`, `updated_at`) VALUES (2, 'Aksi Bersih Sungai', '2026-06-18', 'Kawasan Sungai Ciloseh', 'Kolaborasi warga dan komunitas lingkungan.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `agenda` (`id`, `title`, `date`, `location`, `description`, `created_at`, `updated_at`) VALUES (3, 'Penanaman Pohon Kawasan Perkotaan', '2026-07-05', 'Taman Kota Tasikmalaya', 'Kegiatan penghijauan untuk kualitas udara.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `agenda` AUTO_INCREMENT = 4;
ALTER TABLE `documents` AUTO_INCREMENT = 1;
INSERT INTO `documents` (`id`, `title`, `category`, `filename`, `year`, `description`, `downloads`, `created_at`, `updated_at`) VALUES (1, 'Peraturan Walikota tentang Pengelolaan Lingkungan', 'Peraturan', 'peraturan_walikota.txt', 2026, 'Contoh dokumen regulasi lingkungan hidup.', 0, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `documents` (`id`, `title`, `category`, `filename`, `year`, `description`, `downloads`, `created_at`, `updated_at`) VALUES (2, 'SOP Instalasi Pengelolaan Air Limbah', 'SOP', 'sop_air_limbah.txt', 2026, 'Panduan teknis pengelolaan air limbah.', 0, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `documents` (`id`, `title`, `category`, `filename`, `year`, `description`, `downloads`, `created_at`, `updated_at`) VALUES (3, 'SOP Instalasi Pengendali Emisi', 'SOP', 'sop_pengendali_emisi.txt', 2026, 'Panduan teknis pengendalian emisi.', 0, '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `documents` AUTO_INCREMENT = 4;
ALTER TABLE `gallery` AUTO_INCREMENT = 1;
INSERT INTO `gallery` (`id`, `title`, `image`, `type`, `video_url`, `album`, `description`, `created_at`, `updated_at`) VALUES (1, 'Penghijauan Kota', 'gallery-1.svg', 'foto', NULL, 'Lingkungan', 'Kegiatan penghijauan dan penataan lingkungan.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `gallery` (`id`, `title`, `image`, `type`, `video_url`, `album`, `description`, `created_at`, `updated_at`) VALUES (2, 'Bank Sampah', 'gallery-2.svg', 'foto', NULL, 'Sampah', 'Edukasi ekonomi sirkular melalui bank sampah.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `gallery` (`id`, `title`, `image`, `type`, `video_url`, `album`, `description`, `created_at`, `updated_at`) VALUES (3, 'Edukasi Lingkungan', 'gallery-3.svg', 'foto', NULL, 'Edukasi', 'Kegiatan edukasi bersama masyarakat dan sekolah.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `gallery` (`id`, `title`, `image`, `type`, `video_url`, `album`, `description`, `created_at`, `updated_at`) VALUES (4, 'Video Edukasi Lingkungan', 'video-thumb.svg', 'video', 'https://www.youtube.com/embed/PrV5ERPC9v0', 'Video', 'Video edukasi pengelolaan lingkungan.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `gallery` AUTO_INCREMENT = 5;
ALTER TABLE `links` AUTO_INCREMENT = 1;
INSERT INTO `links` (`id`, `name`, `url`, `description`, `icon`, `created_at`, `updated_at`) VALUES (1, 'Pemerintah Kota Tasikmalaya', 'https://tasikmalayakota.go.id', 'Portal resmi Pemerintah Kota Tasikmalaya.', '🏛', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `links` (`id`, `name`, `url`, `description`, `icon`, `created_at`, `updated_at`) VALUES (2, 'Dinas Binamarga Kota Tasikmalaya', '#', 'Tautan instansi terkait infrastruktur jalan.', '🛣', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `links` (`id`, `name`, `url`, `description`, `icon`, `created_at`, `updated_at`) VALUES (3, 'Dinas Lingkungan Hidup Jawa Barat', 'https://dlh.jabarprov.go.id', 'Portal DLH Provinsi Jawa Barat.', '🌿', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `links` (`id`, `name`, `url`, `description`, `icon`, `created_at`, `updated_at`) VALUES (4, 'Kementerian Lingkungan Hidup', 'https://www.menlhk.go.id', 'Portal kementerian terkait lingkungan hidup.', '🇮🇩', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
INSERT INTO `links` (`id`, `name`, `url`, `description`, `icon`, `created_at`, `updated_at`) VALUES (5, 'Pusat Pengendalian Pembangunan Ekoregion Jawa', '#', 'Tautan pusat pengendalian ekoregion Jawa.', '🗺', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `links` AUTO_INCREMENT = 6;
ALTER TABLE `contacts` AUTO_INCREMENT = 1;
INSERT INTO `contacts` (`id`, `name`, `email`, `subject`, `message`, `status`, `created_at`, `updated_at`) VALUES (1, 'Contoh Warga', 'warga@example.com', 'Informasi layanan', 'Contoh pesan kontak yang sudah tersimpan di database.', 'Baru', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `contacts` AUTO_INCREMENT = 2;
ALTER TABLE `complaints` AUTO_INCREMENT = 1;
INSERT INTO `complaints` (`id`, `ticket_number`, `name`, `email`, `phone`, `category`, `location`, `message`, `status`, `admin_response`, `created_at`, `updated_at`) VALUES (1, 'DLH-2026-00001', 'Contoh Pelapor', 'pelapor@example.com', '081234567890', 'Sampah', 'Kota Tasikmalaya', 'Contoh pengaduan sampah yang masuk ke database.', 'Masuk', 'Belum ada respon admin.', '2026-06-03 07:08:58.782288', '2026-06-03 07:08:58.782288');
ALTER TABLE `complaints` AUTO_INCREMENT = 2;
ALTER TABLE `visitor_logs` AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS = 1;
