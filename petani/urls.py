from django.urls import path
from .import views

urlpatterns = [
    path('beranda/', views.beranda, name='beranda'),
    
    
    # Tambahan fitur lain yang sebelumnya sudah ada (opsional, jika belum diatur)
    path('profil', views.profil, name='profil'),
    path('profil-kantor/', views.profil_kantor, name='profil_kantor'),
    path('profil-ketua/', views.profil_ketua, name='profil_ketua'),
    
    path('kegiatan/', views.kegiatan_list, name='kegiatan_list'),
    
    path('grup', views.grup, name='grup'),
    
    path('ketua/', views.ketua, name='ketua'),
    path('anggota', views.anggota, name='anggota'),
    
    path('alsintan', views.alsintan, name='alsintan'),
    path('alsintan/tambah/', views.tambah_alsintan, name='tambah_alsintan'),
    path('alsintan/edit/<int:id>/', views.edit_alsintan, name='edit_alsintan'),
    path('alsintan/hapus/<int:id>/', views.hapus_alsintan, name='hapus_alsintan'),
    
    path('lahan', views.lahan, name='lahan'),
    path('lahan/tambah/', views.tambah_lahan, name='tambah_lahan'),
    path('edit-lahan/<int:id>/', views.edit_lahan, name='edit_lahan'),
    
    path('erdkk/', views.erdkk, name='erdkk'),
    path('ajukan-sppt/', views.ajukan_sppt, name='ajukan_sppt'),
    
    path('tanaman', views.tanaman, name='tanaman'),
    
    # Forum Diskusi
    path('forum/', views.daftar_forum, name='daftar_forum'),
    path('forum/<int:forum_id>/', views.detail_forum, name='detail_forum'),
    path('forum/buat/', views.buat_forum, name='buat_forum'),
    path('forum/hapus/<int:pk>/', views.hapus_forum, name='hapus_forum'),
    path('komentar/hapus/<int:pk>/', views.hapus_komentar, name='hapus_komentar'),
    
    
    #login

    path('login/', views.login_view, name='login'),
    path('logout', views.logoutPage, name='logoutPage'),
]
