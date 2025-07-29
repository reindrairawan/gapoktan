from django.urls import path
from .import views

urlpatterns = [
    path('beranda/', views.dashboard, name='beranda_admin'),
    path('unduh-laporan/', views.unduh_laporan_pdf, name='unduh_laporan'),
    
    path('profil/', views.profiladmin, name='profiladmin'),
    path('form-profil/', views.formprofiladmin, name='formprofiladmin'),
    path('edit-profil/<str:pk>', views.editprofiladmin, name='editprofiladmin'),
    path('delete-profil/<str:pk>', views.deleteprofiladmin, name='deleteprofiladmin'),
    
    # kegiatan
    
    path('form-kegiatan/', views.formkegiatanadmin, name='formkegiatanadmin'),
    path('edit-kegiatan/<str:pk>/', views.editkegiatanadmin, name='editkegiatanadmin'),
    path('delete-kegiatan/<str:pk>/', views.deletekegiatanadmin, name='deletekegiatanadmin'),
    
    #grup
    
    path('grup/', views.grupadmin, name='grupadmin'),
    path('form-grup/', views.formgrupadmin, name='formgrupadmin'),
    path('edit-grup/<str:pk>', views.editgrupadmin, name='editgrupadmin'),
    path('delete-grup/<str:pk>', views.deletegrupadmin, name='deletegrupadmin'),
    
    #ketua
    
    path('ketua/', views.ketuaadmin, name='ketuaadmin'),
    path('form-ketua/', views.formketuaadmin, name='formketuaadmin'),
    path('edit-ketua/<str:pk>', views.editketuaadmin, name='editketuaadmin'),
    path('delete-ketua/<str:pk>', views.deleteketuaadmin, name='deleteketuaadmin'),
    
    #ketua gapoktan
    
    path('form-ketuagapoktan/', views.formketuagapoktanadmin, name='formketuagapoktanadmin'),
    path('edit-ketuagapoktan/<str:pk>/', views.editketuagapoktanadmin, name='editketuagapoktanadmin'),
    path('delete-ketuagapoktan/<str:pk>/', views.deleteketuagapoktanadmin, name='deleteketuagapoktanadmin'),
    
    #anggota
    
    path('anggota/', views.anggotaadmin, name='anggotaadmin'),
    path('form-anggota/', views.formanggotaadmin, name='formanggotaadmin'),
    path('edit-anggota/<str:pk>', views.editanggotaadmin, name='editanggotaadmin'),
    path('delete-anggota/<str:pk>', views.deleteanggotaadmin, name='deleteanggotaadmin'),
    path('import-anggota/', views.import_anggota_excel, name='import_anggota_excel'),
    
    
    #alsintan
    
    path('alsintan/', views.alsintanadmin, name='alsintanadmin'),
    path('form-alsintan/', views.formalsintanadmin, name='formalsintanadmin'),
    path('edit-alsintan/<str:pk>', views.editalsintanadmin, name='editalsintanadmin'),
    path('delete-alsintan/<str:pk>', views.deletealsintanadmin, name='deletealsintanadmin'),
    
    #Lahan
    
    path('lahan/', views.lahanadmin, name='lahanadmin'),
    path('form-lahan/', views.formlahanadmin, name='formlahanadmin'),
    path('edit-lahan/<str:pk>', views.editlahanadmin, name='editlahanadmin'),
    path('delete-lahan/<str:pk>', views.deletelahanadmin, name='deletelahanadmin'),
    
    #e RDKK
    
    path('erdkk/', views.erdkkadmin, name='erdkkadmin'),
    path('form-erdkk/', views.formerdkkadmin, name='formerdkkadmin'),
    path('edit-erdkk/<str:pk>', views.editerdkkadmin, name='editerdkkadmin'),
    path('delete-erdkk/<str:pk>', views.deleteerdkkadmin, name='deleteerdkkadmin'),
    path('erdkk/import-excel/', views.import_erdkk_excel, name='import_erdkk_excel'),
    
    # sppt
    
    path('form-sppt/', views.formspptadmin, name='formspptadmin'),
    path('edit-sppt/<str:pk>/', views.editspptadmin, name='editspptadmin'),
    path('delete-sppt/<str:pk>/', views.deletespptadmin, name='deletespptadmin'),
    
    # penyakit tanaman
    path('penyakittanaman/', views.penyakittanamanadmin, name='penyakittanamanadmin'),
    path('form-penyakittanaman/', views.formpenyakittanamanadmin, name='formpenyakittanamanadmin'),
    path('edit-penyakittanaman/<str:pk>', views.editpenyakittanamanadmin, name='editpenyakittanamanadmin'),
    path('delete-penyakittanaman/<str:pk>', views.deletepenyakittanamanadmin, name='deletepenyakittanamanadmin'),

    path('login/', views.login_view, name='login'),
    path('logout', views.logoutPage, name='logoutPage'),
]
