from django import forms
from .models import ProfilGapoktan, Kegiatan, Grup, KetuaPoktan, KetuaGapoktan, Petani, Alsintan, Lahan, DataERDKK, Sppt, PenyakitTanaman
from django.utils.text import slugify

class ProfilGapoktanForm(forms.ModelForm):
    class Meta:
        model = ProfilGapoktan
        fields = ['gambar_kantor', 'deskripsi_kantor', 'gambar_ketua', 'deskripsi_ketua']
        
        widgets = {
            'gambar_kantor': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
            'deskripsi_kantor': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan deskripsi kantor...',
                'rows': 4,
            }),
            'gambar_ketua': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
            'deskripsi_ketua': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan deskripsi ketua...',
                'rows': 4,
            }),
        }

        labels = {
            'gambar_kantor': 'Gambar Kantor',
            'deskripsi_kantor': 'Deskripsi Kantor',
            'gambar_ketua': 'Gambar Ketua',
            'deskripsi_ketua': 'Deskripsi Ketua',
        }


class KegiatanForm(forms.ModelForm):
    class Meta:
        model = Kegiatan
        fields = ['judul', 'tanggal', 'deskripsi', 'gambar']
        
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Judul kegiatan',
            }),
            'tanggal': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'rows': 4,
                'placeholder': 'Deskripsi kegiatan',
            }),
            'gambar': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
        }

        labels = {
            'judul': 'Judul Kegiatan',
            'tanggal': 'Tanggal',
            'deskripsi': 'Deskripsi',
            'gambar': 'Dokumentasi / Gambar',
        }
        
class GrupForm(forms.ModelForm):
    class Meta:
        model = Grup
        fields = ['nama', 'aktif']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-input border rounded w-full',
                'placeholder': 'Masukkan nama grup'
            }),
            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Auto generate slug from nama
        instance.slug = slugify(self.cleaned_data['nama'])
        if commit:
            instance.save()
        return instance
    
class KetuaPoktanForm(forms.ModelForm):
    class Meta:
        model = KetuaPoktan
        fields = ['grup', 'nama', 'nik', 'alamat']

        widgets = {
            'grup': forms.Select(attrs={  # PERBAIKI INI!
                'class': 'select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),

            'nama': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Nama Ketua Kelompok',
            }),
            'nik': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'NIK',
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Alamat Ketua Kelompok',
            }),
        }

        labels = {
            'grup': 'Grup Tani',
            'nama': 'Nama Ketua',
            'nik': 'NIK',
            'alamat': 'Alamat',
        }


class KetuaGapoktanForm(forms.ModelForm):
    class Meta:
        model = KetuaGapoktan
        fields = ['grup', 'nama', 'nik', 'alamat']

        widgets = {
            'grup': forms.SelectMultiple(attrs={  # PERBAIKI INI!
                'class': 'select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-green-200',
            }),
            'nama': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-green-200',
                'placeholder': 'Nama Ketua Gapoktan',
            }),
            'nik': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-green-200',
                'placeholder': 'NIK',
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-green-200',
                'rows': 3,
                'placeholder': 'Alamat Ketua Gapoktan',
            }),
        }

        labels = {
            'grup': 'Grup Gapoktan',
            'nama': 'Nama Ketua',
            'nik': 'NIK',
            'alamat': 'Alamat',
        }



class PetaniForm(forms.ModelForm):
    class Meta:
        model = Petani
        fields = ['grup', 'nama', 'nik', 'alamat']

        widgets = {
            'grup': forms.Select(attrs={
                'class': 'select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),

            'nama': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Nama Ketua Kelompok',
            }),
            'nik': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'NIK',
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Alamat Ketua Kelompok',
            }),
        }

        labels = {
            'grup': 'Grup Tani',
            'nama': 'Nama Ketua',
            'nik': 'NIK',
            'alamat': 'Alamat',
        }
        

class AlsintanForm(forms.ModelForm):
    class Meta:
        model = Alsintan
        fields = [
            'nama_alat', 'pemilik', 'jumlah', 'kondisi','tanggal_pengadaan', 'sumber_dana', 'dokumentasi', 'keterangan'
        ]

        widgets = {
            'nama_alat': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Nama Alat Pertanian',
            }),
            'pemilik': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Jenis Alat',
            }),
            'jumlah': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Jumlah Unit',
            }),
            'kondisi': forms.Select(attrs={
                'class': 'select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),
            'tanggal_pengadaan': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),
            'sumber_dana': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Contoh: Dana Desa, APBD, dll',
            }),
            'dokumentasi': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full',
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Keterangan tambahan (opsional)',
            }),
        }

        labels = {
            'nama_alat': 'Nama Alat',
            'jenis_alat': 'Jenis Alat',
            'jumlah': 'Jumlah',
            'kondisi': 'Kondisi',
            'tanggal_pengadaan': 'Tanggal Pengadaan',
            'sumber_dana': 'Sumber Dana',
            'dokumentasi': 'Foto/Dokumentasi',
            'keterangan': 'Keterangan',
        }

class LahanForm(forms.ModelForm):
    class Meta:
        model = Lahan
        fields = ['pemilik', 'gambar_lahan', 'luas', 'jenis_tanaman', 'lokasi', 'latitude', 'longitude','tanggal_tanam','tanggal_panen']

        widgets = {
            'pemilik': forms.Select(attrs={
                'class': 'select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),
            'gambar_lahan': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
            }),
            'luas': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Luas lahan (contoh: 2 hektar)',
            }),
            'jenis_tanaman': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Jenis tanaman (contoh: Padi, Jagung)',
            }),
            'lokasi': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Deskripsi lokasi lahan',
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Latitude (contoh: -7.123456)',
                'step': 'any',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Longitude (contoh: 113.123456)',
                'step': 'any',
            }),
            'tanggal_tanam': forms.DateInput(attrs={
                'class': 'date-input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'type': 'date',
            }),
            'tanggal_panen': forms.DateInput(attrs={
                'class': 'date-input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'type': 'date',
            }),
        }

        labels = {
            'pemilik': 'Pemilik Lahan',
            'gambar_lahan': 'Gambar Lahan',
            'luas': 'Luas Lahan',
            'jenis_tanaman': 'Jenis Tanaman',
            'lokasi': 'Deskripsi Lokasi',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'tanggal_tanam':'tanggal_tanam',
            'tanggal_panen':'tanggal_panen',
        }

 

class DataERDKKForm(forms.ModelForm):
    class Meta:
        model = DataERDKK
        fields = [
            'petani',
            'komoditas',
            'luas_lahan',
            'pupuk_urea',
            'pupuk_npk',
            'pupuk_organik',
            'tahun_rencana'
        ]

        widgets = {
            'petani': forms.Select(attrs={
                'class': 'select mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2'
            }),
            'komoditas': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan nama komoditas...'
            }),
            'luas_lahan': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Contoh: 2.5 Ha'
            }),
            'pupuk_urea': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan kebutuhan pupuk Urea (kg)'
            }),
            'pupuk_npk': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan kebutuhan pupuk NPK (kg)'
            }),
            'pupuk_organik': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'placeholder': 'Masukkan kebutuhan pupuk Organik (kg)'
            }),
            'tahun_rencana': forms.NumberInput(attrs={
                'class': 'input mt-1 block w-full rounded-md border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 py-2',
                'min': 2000,
                'placeholder': 'Masukkan tahun rencana'
            }),
        }

        labels = {
            'petani': 'Nama Petani',
            'komoditas': 'Komoditas',
            'luas_lahan': 'Luas Lahan (Ha)',
            'pupuk_urea': 'Kebutuhan Pupuk Urea (Kg)',
            'pupuk_npk': 'Kebutuhan Pupuk NPK (Kg)',
            'pupuk_organik': 'Kebutuhan Pupuk Organik (Kg)',
            'tahun_rencana': 'Tahun Rencana',
        }


class SpptForm(forms.ModelForm):
    class Meta:
        model = Sppt
        fields = ['nama_petani', 'fotokopi_ktp', 'fotokopi_kk', 'fotokopi_sppt', 'nama_ibu', 'status', 'catatan']

        widgets = {
            'nama_petani': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Nama petani',
            }),
            'nama_ibu': forms.TextInput(attrs={
                'class': 'input mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200',
                'placeholder': 'Nama ibu kandung',
            }),
            'fotokopi_ktp': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
            'fotokopi_kk': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
            'fotokopi_sppt': forms.ClearableFileInput(attrs={
                'class': 'file-input mt-1 block w-full text-gray-700 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 py-2',
            }),
            'status': forms.Select(choices=Sppt.STATUS_CHOICES, attrs={
                'class': 'form-select mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-blue-200'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'textarea mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring focus:ring-red-200',
                'placeholder': 'Tulis alasan jika ditolak (opsional)',
                'rows': 3,
            }),
        }

        labels = {
            'nama_petani': 'Nama Petani',
            'fotokopi_ktp': 'Upload Fotokopi KTP',
            'fotokopi_kk': 'Upload Fotokopi KK',
            'fotokopi_sppt': 'Upload Fotokopi SPPT',
            'nama_ibu': 'Nama Ibu Kandung',
            'status': 'Status Pengajuan',
            'catatan': 'Catatan (isi alasan jika ditolak)',
        }
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        catatan = cleaned_data.get('catatan')

        if status == 'ditolak' and not catatan:
            self.add_error('catatan', 'Harap isi alasan penolakan di kolom catatan.')

class PenyakitTanamanForm(forms.ModelForm):
    class Meta:
        model = PenyakitTanaman
        fields = '__all__'