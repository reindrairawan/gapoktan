from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from datetime import date, datetime
from django.utils import timezone 
from django.contrib.auth.models import User

class ProfilGapoktan(models.Model):
    nama_instansi = models.CharField(max_length=100, default="Gapoktan Mlandingan")
    gambar_kantor = models.ImageField(upload_to='gambar/profil/kantor/', null=True, blank=True)
    deskripsi_kantor = RichTextField(null=True, blank=True)
    gambar_ketua = models.ImageField(upload_to='gambar/profil/ketua/', null=True, blank=True)
    deskripsi_ketua = RichTextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Data Profil Gapoktan"

    def __str__(self):
        return self.nama_instansi
    
class Kegiatan(models.Model):
    judul = models.CharField(max_length=200)
    tanggal = models.DateField()
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='kegiatan/', blank=True, null=True)
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)

    def __str__(self):
        return f"{self.judul} ({self.tanggal.strftime('%d-%m-%Y')})"

    class Meta:
        verbose_name_plural = "Data Kegiatan"
        ordering = ['-tanggal']
        
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.judul) 
        return super().save(*args, **kwargs)



class Grup(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    aktif = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, null=True,blank=True, unique=True)

    
    class Meta:
        verbose_name_plural ="Data Grup"
        
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.nama) 
        return super().save(*args, **kwargs)

class KetuaPoktan(models.Model):
    grup = models.ForeignKey(Grup, on_delete=models.CASCADE, related_name='ketua_poktan')
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=100, default="0000000000000000")
    alamat = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)
    
    class Meta:
        verbose_name_plural ="Data Ketua Kelompok"
        
    def __str__(self):
        return self.nama
    
    def nik_tersembunyi(self):
        return self.nik[:-4].replace(self.nik[:-4], '*' * len(self.nik[:-4])) + self.nik[-4:]
    
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.nama) 
        return super().save(*args, **kwargs)
    
    
class KetuaGapoktan(models.Model):
    grup = models.ManyToManyField(Grup, related_name='ketua_gapoktan')
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=100, default="0000000000000000")
    alamat = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)
    class Meta:
        verbose_name_plural = "Ketua Gapoktan"

    def __str__(self):
        return self.nama

    def nik_tersembunyi(self):
        return self.nik[:-4].replace(self.nik[:-4], '*' * len(self.nik[:-4])) + self.nik[-4:]
    
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.nama) 
        return super().save(*args, **kwargs)
    
    
    
class Petani(models.Model):
    grup = models.ForeignKey(Grup, on_delete=models.CASCADE, related_name='anggota')
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=100, default="0000000000000000")
    alamat = RichTextField(blank=True, null=True)
    created_at = models.DateField(default=timezone.now) 
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)
    class Meta:
        verbose_name_plural ="Data Petani"
    
    def __str__(self):
        return self.nama
    
    def nik_tersembunyi(self):
        return self.nik[:-4].replace(self.nik[:-4], '*' * len(self.nik[:-4])) + self.nik[-4:]
    
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.nama) 
        return super().save(*args, **kwargs)
        
    
class Alsintan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alsintan', null=True, blank=True)
    STATUS_CHOICES = [
        ('tersedia', 'Tersedia'),
        ('dipinjam', 'Dipinjam'),
        ('rusak', 'Rusak'),
    ]
    nama_alat = models.CharField(max_length=100)
    pemilik = models.CharField(max_length=100)
    jumlah = models.PositiveIntegerField(default=1)
    kondisi = models.CharField(max_length=10, choices=STATUS_CHOICES, default='tersedia')
    tanggal_pengadaan = models.DateField()
    sumber_dana = models.CharField(max_length=100, blank=True, null=True)
    dokumentasi = models.ImageField(upload_to='gambar/alsintan/', blank=True, null=True)
    keterangan = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)

    class Meta:
        verbose_name_plural = "Data Alsintan"

    def __str__(self):
        return f"{self.nama_alat} - {self.jenis_alat}"
    
    def save(self, *args, **kwargs):  # new 
        if not self.slug: 
            self.slug = slugify(self.nama_alat) 
        return super().save(*args, **kwargs)

class Lahan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lahan', null=True, blank=True)
    pemilik = models.ForeignKey(Petani, on_delete=models.CASCADE)
    gambar_lahan = models.ImageField(upload_to='gambar/lahan', blank=False, null=True)
    luas = models.CharField(max_length=20) 
    jenis_tanaman = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tanggal_tanam = models.DateField(null=True, blank=True)
    tanggal_panen = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [
        ('tertunda', 'Tertunda'),
        ('berhasil', 'Berhasil'),
        ('gagal', 'Gagal'),
    ]
    status_panen = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tertunda')
    created_at = models.DateField(default=timezone.now) 
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)
    class Meta:
        verbose_name_plural ="Data Lahan"
        
    def __str__(self):
        return self.pemilik.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.pemilik.nama}-{self.jenis_tanaman}")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.slug = f"{base_slug}-{timestamp}"
        return super().save(*args, **kwargs)
    
    @property
    def progress_tanam(self):
        if self.tanggal_tanam and self.tanggal_panen:
            total_days = (self.tanggal_panen - self.tanggal_tanam).days
            passed_days = (timezone.now().date() - self.tanggal_tanam).days
            if total_days > 0:
                progress = min(100, max(0, int((passed_days / total_days) * 100)))
                return progress
        return 0
    
class DataERDKK(models.Model):
    petani = models.ForeignKey('Petani', on_delete=models.CASCADE)
    komoditas = models.CharField(max_length=100)
    luas_lahan = models.CharField(max_length=20)
    pupuk_urea = models.FloatField(default=0)
    pupuk_npk = models.FloatField(default=0)
    pupuk_organik = models.FloatField(default=0)
    tahun_rencana = models.PositiveIntegerField(default=date.today().year)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Data ERDKK"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.petani.nama}-{self.komoditas}-{self.tahun_rencana}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.petani.nama} - {self.komoditas} ({self.tahun_rencana})"
    
class Sppt(models.Model):
    STATUS_CHOICES = [
        ('proses', 'Diproses'),
        ('diterima', 'Diterima'),
        ('ditolak', 'Ditolak'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    nama_petani = models.CharField(max_length=100, default="Tidak Diketahui")
    fotokopi_ktp = models.ImageField(upload_to='pengajuan/ktp/')
    fotokopi_kk = models.ImageField(upload_to='pengajuan/kk/')
    fotokopi_sppt = models.ImageField(upload_to='pengajuan/sppt/')
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)
    nama_ibu = models.CharField(max_length=100, default="Tidak Diketahui")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proses')  # 👈 Tambahan baru
    catatan = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Pengajuan atas nama {self.nama_petani}"

    class Meta:
        verbose_name_plural = "Data Sppt"


    
class PenyakitTanaman(models.Model):
    lahan = models.ForeignKey(Lahan, on_delete=models.CASCADE)
    penyakit = models.CharField(max_length=100)
    gambar_tanaman = models.ImageField(upload_to='gambar/tanaman', blank=False, null=True)
    
    class Meta:
        verbose_name_plural ="Data Penyakit Tanaman"
        
class ForumDiskusi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_diskusi')
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Forum Diskusi"

    def __str__(self):
        return self.judul


class KomentarDiskusi(models.Model):
    forum = models.ForeignKey(ForumDiskusi, on_delete=models.CASCADE, related_name='komentar')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='komentar_diskusi')
    isi = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Komentar Diskusi"

    def __str__(self):
        return f"Komentar oleh {self.user.username} di {self.forum.judul}"
