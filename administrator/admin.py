from django.contrib import admin
from .models import  ProfilGapoktan, Kegiatan, Grup, KetuaPoktan, KetuaGapoktan, Petani, Alsintan, Lahan, DataERDKK, Sppt, PenyakitTanaman,  ForumDiskusi, KomentarDiskusi
from django.utils.html import format_html

@admin.register(ProfilGapoktan)
class ProfilGapoktanAdmin(admin.ModelAdmin):
    list_display=('id', 'gambar_kantor', 'deskripsi_kantor', 'gambar_ketua', 'deskripsi_ketua', 'updated_at',)

@admin.register(Kegiatan)
class KegiatanAdmin(admin.ModelAdmin):
    list_display = ('id','judul', 'tanggal', 'preview_gambar','slug',)
    search_fields = ('judul', 'deskripsi')
    list_filter = ('tanggal',)
    ordering = ('-tanggal',)

    def preview_gambar(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" width="80" style="border-radius: 6px;" />', obj.gambar.url)
        return "-"
    preview_gambar.short_description = "Dokumentasi"
    
@admin.register(Grup)
class GrupAdmin(admin.ModelAdmin):
    list_display=('id', 'nama', 'aktif','slug',)
    prepopulated_fields = {"slug": ("nama",)} 

@admin.register(KetuaPoktan)
class KetuaPoktanAdmin(admin.ModelAdmin):
    list_display = ('id', 'grup', 'nama', 'nik', 'alamat', 'slug')
    prepopulated_fields = {"slug": ("nama",)}

@admin.register(KetuaGapoktan)
class KetuaGapoktanAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_grup', 'nama', 'nik_tersembunyi', 'alamat', 'slug')
    prepopulated_fields = {"slug": ("nama",)}

    def get_grup(self, obj):
        return ", ".join([g.nama_grup for g in obj.grup.all()])  

    
@admin.register(Petani)
class PetaniAdmin(admin.ModelAdmin):
    list_display=('id', 'grup', 'nama', 'nik', 'alamat','slug')
    prepopulated_fields = {"slug": ("nama",)} 

@admin.register(Alsintan)
class AlsintanAdmin(admin.ModelAdmin):
    list_display = ('id','nama_alat','pemilik','jumlah','kondisi','tanggal_pengadaan','sumber_dana','slug')
    search_fields = ('nama_alat', 'pemilik')
    list_filter = ('kondisi', 'tanggal_pengadaan')

    
@admin.register(Lahan)
class LahanAdmin(admin.ModelAdmin):
    list_display=('id', 'pemilik', 'gambar_lahan', 'luas', 'jenis_tanaman', 'lokasi','latitude','longitude', 'tanggal_tanam', 'tanggal_panen', 'progress_tanam', 'status_panen','slug')
    prepopulated_fields = {"slug": ("pemilik",)} 
    
@admin.register(DataERDKK)
class DataERDKKAdmin(admin.ModelAdmin):
    list_display = ('petani','komoditas','luas_lahan','pupuk_urea','pupuk_npk','pupuk_organik','tahun_rencana','slug')
    search_fields = ('petani__nama', 'komoditas')
    list_filter = ('tahun_rencana', 'komoditas')
    prepopulated_fields = {"slug": ("komoditas",)}

    
@admin.register(Sppt)
class SpptAdmin(admin.ModelAdmin):
    list_display = ( 'nama_petani','fotokopi_ktp', 'fotokopi_kk', 'fotokopi_sppt', 'nama_ibu', 'tanggal_pengajuan','status')
    list_filter = ('status',)
    readonly_fields = ('tanggal_pengajuan',)
    
@admin.register(PenyakitTanaman)
class PenyakitTanamanAdmin(admin.ModelAdmin):
    list_display=('id', 'lahan', 'penyakit', 'gambar_tanaman',)
    
class KomentarDiskusiInline(admin.TabularInline):
    model = KomentarDiskusi
    extra = 1
    verbose_name_plural = "Komentar"

@admin.register(ForumDiskusi)
class ForumDiskusiAdmin(admin.ModelAdmin):
    list_display = ("judul", "user", "tanggal")
    search_fields = ("judul", "isi", "user__username")
    ordering = ("-tanggal",)
    inlines = [KomentarDiskusiInline]


@admin.register(KomentarDiskusi)
class KomentarDiskusiAdmin(admin.ModelAdmin):
    list_display = ("forum", "user", "tanggal")
    search_fields = ("forum__judul", "isi", "user__username")
    ordering = ("-tanggal",)