-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 16, 2019 at 10:59 AM
-- Server version: 5.5.54-MariaDB-1ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ta_spdp`
--

-- --------------------------------------------------------

--
-- Table structure for table `accept`
--

CREATE TABLE `accept` (
  `no_sprint` varchar(20) NOT NULL,
  `no_laporan` varchar(20) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(40) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `tempat_lahir` varchar(30) NOT NULL,
  `tanggal_lahir` varchar(30) NOT NULL,
  `pekerjaan` varchar(40) NOT NULL,
  `agama` varchar(30) NOT NULL,
  `kewarganegaraan` varchar(30) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `kategori` varchar(30) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `penerima` varchar(50) NOT NULL,
  `tampil_tgl` varchar(15) NOT NULL,
  `kapolsek` varchar(50) NOT NULL,
  `nrp` varchar(50) NOT NULL,
  `tgl_cek` varchar(15) NOT NULL,
  `bts_penyidikan` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `data_diterima`
--

CREATE TABLE `data_diterima` (
  `no_sprint` varchar(30) NOT NULL,
  `no_laporan` varchar(30) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `tgl_diterima` varchar(30) NOT NULL,
  `tgl_disetujui` varchar(30) NOT NULL,
  `keterangan` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `data_penyidik`
--

CREATE TABLE `data_penyidik` (
  `nm_penyidik` varchar(50) NOT NULL,
  `nrp` varchar(30) NOT NULL,
  `jbt_penyidik` varchar(30) NOT NULL,
  `alamat_penyidik` varchar(70) NOT NULL,
  `t_lahir` varchar(50) NOT NULL,
  `tgl_lahir` varchar(40) NOT NULL,
  `no_tlp` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `data_penyidik`
--

INSERT INTO `data_penyidik` (`nm_penyidik`, `nrp`, `jbt_penyidik`, `alamat_penyidik`, `t_lahir`, `tgl_lahir`, `no_tlp`) VALUES
('Suhanto S.kom', '15362366', 'Penyidik', 'jl. haji mabrur surabya', 'surabaya', '07-05-1969', '083757677665'),
('Abd. Somad S.H', '25137583', 'Penyidik', 'Ds. krembung', 'Sidoarjo', '13-09-1971', '087783674234'),
('Okta Avie S.H', '32879144', 'Penyidik', 'Ds. Jabon , sidoarjo', 'Sidoarjo', '24-02-1967', '083849057899'),
('Waliyadin S.T', '47677241', 'Penyidik', 'Candi Sidoarjo', 'Sidoarjo', '16-04-1975', '082268414622'),
('H. Suwito', '58127631', 'Penyidik', 'Rangka Kidul', 'Blitar', '29-11-1972', '083527573621'),
('Arif Juliawan', '63126412', 'Penyidik', 'Tanggulangin', 'Sidoarjo', '12-08-1969', '085286123833'),
('Yudhi Setiawan', '77125152', 'Penyidikan', 'Penyakit', 'Malang', '07-12-1973', '085643129874'),
('Fahrul S.', '89727544', 'Penyidik', 'Candi', 'Tulungagung', '26-03-1974', '081421224142');

-- --------------------------------------------------------

--
-- Table structure for table `data_reject`
--

CREATE TABLE `data_reject` (
  `no_sprint` varchar(30) NOT NULL,
  `no_laporan` varchar(30) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(40) NOT NULL,
  `kategori` varchar(40) NOT NULL,
  `pasal` varchar(40) NOT NULL,
  `tgl_reject` varchar(30) NOT NULL,
  `alasan` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `det_penyidik`
--

CREATE TABLE `det_penyidik` (
  `no_sprint` varchar(30) NOT NULL,
  `nrp` varchar(20) NOT NULL,
  `nm_penyidik` varchar(50) NOT NULL,
  `jbt_penyidik` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `logaktivitas`
--

CREATE TABLE `logaktivitas` (
  `tgl_aktivitas` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `ip` varchar(30) NOT NULL,
  `keterangan` varchar(30) NOT NULL,
  `no_sprint` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `logaktivitas`
--

INSERT INTO `logaktivitas` (`tgl_aktivitas`, `username`, `ip`, `keterangan`, `no_sprint`) VALUES
('2019-07-10 15:49:20', 'Polsek Candi', '127.0.0.1', 'Create', '17'),
('2019-07-21 21:07:44', 'Polsek Candi', '127.0.0.1', 'Create', '4123'),
('2019-07-24 22:54:30', 'Polsek Candi', '127.0.0.1', 'Create', '4677'),
('2019-07-24 22:58:29', 'Polsek Candi', '127.0.0.1', 'Create', '9897'),
('2019-08-13 14:44:27', 'Polsek Candi', '127.0.0.1', 'Create', '321'),
('2019-08-15 12:18:20', 'Polsek Candi', '127.0.0.1', 'Create', '1');

-- --------------------------------------------------------

--
-- Table structure for table `notifspdp`
--

CREATE TABLE `notifspdp` (
  `no_sprint` varchar(20) NOT NULL,
  `no_laporan` varchar(20) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(40) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `tempat_lahir` varchar(30) NOT NULL,
  `tanggal_lahir` varchar(30) NOT NULL,
  `pekerjaan` varchar(40) NOT NULL,
  `agama` varchar(30) NOT NULL,
  `kewarganegaraan` varchar(30) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `kategori` varchar(30) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `penerima` varchar(50) NOT NULL,
  `tanggal` varchar(20) NOT NULL,
  `tampil_tgl` varchar(15) NOT NULL,
  `kapolsek` varchar(50) NOT NULL,
  `nrp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `notif_jaksa`
--

CREATE TABLE `notif_jaksa` (
  `no_sprint` varchar(30) NOT NULL,
  `no_laporan` varchar(30) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `tgl_terkirim` varchar(30) NOT NULL,
  `tgl_cek` varchar(30) NOT NULL,
  `keterangan` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `profil_kapolsek`
--

CREATE TABLE `profil_kapolsek` (
  `nama_kapolsek` varchar(40) NOT NULL,
  `jabatan_kapolsek` varchar(40) NOT NULL,
  `nrp_kapolsek` varchar(40) NOT NULL,
  `alamat_kapolsek` varchar(70) NOT NULL,
  `tempat_tanggal_lahir` varchar(70) NOT NULL,
  `photo_profile` varchar(40) NOT NULL,
  `photo_ttd` varchar(40) NOT NULL,
  `kode` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profil_kapolsek`
--

INSERT INTO `profil_kapolsek` (`nama_kapolsek`, `jabatan_kapolsek`, `nrp_kapolsek`, `alamat_kapolsek`, `tempat_tanggal_lahir`, `photo_profile`, `photo_ttd`, `kode`) VALUES
('HERU MURSALNNYOTO, S.H, M.H', 'AJUN KOMISARIS POLISI', '42358731', 'NGANJUK', '13-05-1977', 'fariz-1.png', '1563176014292.png', '');

-- --------------------------------------------------------

--
-- Table structure for table `reject`
--

CREATE TABLE `reject` (
  `no_sprint` varchar(30) NOT NULL,
  `no_laporan` varchar(30) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(40) NOT NULL,
  `kategori` varchar(40) NOT NULL,
  `pasal` varchar(40) NOT NULL,
  `tgl_reject` varchar(30) NOT NULL,
  `alasan` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `spdp`
--

CREATE TABLE `spdp` (
  `no_sprint` varchar(20) NOT NULL,
  `no_laporan` varchar(20) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(40) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `tempat_lahir` varchar(30) NOT NULL,
  `tanggal_lahir` varchar(30) NOT NULL,
  `pekerjaan` varchar(40) NOT NULL,
  `agama` varchar(30) NOT NULL,
  `kewarganegaraan` varchar(30) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `kategori` varchar(30) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `penerima` varchar(50) NOT NULL,
  `tanggal` varchar(20) NOT NULL,
  `tampil_tgl` varchar(15) NOT NULL,
  `kapolsek` varchar(50) NOT NULL,
  `nrp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `no_sprint` varchar(30) NOT NULL,
  `no_laporan` varchar(30) NOT NULL,
  `no_pol` varchar(30) NOT NULL,
  `nama_tsk` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `pasal` varchar(50) NOT NULL,
  `tgl_terkirim` varchar(30) NOT NULL,
  `tgl_cek` varchar(30) NOT NULL,
  `keterangan` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `nama` varchar(50) NOT NULL,
  `alamat` varchar(70) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(40) NOT NULL,
  `level_akses` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`nama`, `alamat`, `username`, `password`, `email`, `level_akses`) VALUES
('Fariz Mufarrizal', 'candi', 'fariz', '123', 'fariz@gamil.com', 1),
('fita widyawati', 'sidoarjo', 'fita', '321', 'fita@gmail.com', 2),
('hadi ismanto', 'candi', 'hadi', '456', 'hadi@gmail.com', 3);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
