from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator
from administrator.models import (ProfilGapoktan, Kegiatan, Alsintan, Lahan, Grup, KetuaPoktan, KetuaGapoktan, Petani, DataERDKK, Sppt, PenyakitTanaman, ForumDiskusi, KomentarDiskusi)
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import OTPForm
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import os

# # Initialize Firebase app and Firestore client if not already initialized
# if not firebase_admin._apps:
#     cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'aplikasi', 'serviceAccountKey.json')
#     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)
# db = firestore.client()

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Konfigurasi dari environment variables
            firebase_config = {
                "type": os.environ.get("FIREBASE_TYPE"),
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
            }
            
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            raise RuntimeError(f"Gagal inisialisasi Firebase: {str(e)}")

# Inisialisasi Firestore client
try:
    db = initialize_firebase()
except Exception as e:
    # Handle error sesuai kebutuhan aplikasi
    print(f"Error Firebase: {e}")
    db = None  # Atau fallback ke sistem lain
    
def login_view(request):
    if request.method == 'POST':
        nik = request.POST.get('nik')
        password_input = request.POST.get('password')
        print("NIK:", nik)

        docs = db.collection('user').where('nik', '==', nik).stream()
        user_data = None
        for doc in docs:
            user_data = doc.to_dict()
            break

        if user_data:
            # Ambil password dari Firebase (pastikan memang disimpan di sana)
            password_stored = user_data.get('password')

            if password_input == password_stored:
                user, created = User.objects.get_or_create(username=nik)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                request.session['username'] = user_data.get('username', '')
                request.session['role'] = user_data.get('role', '')

                if user_data.get('role') == 'admin':
                    return redirect('beranda_admin')
                else:
                    return redirect('beranda')
            else:
                messages.error(request, 'Password salah.')
        else:
            messages.error(request, 'NIK tidak ditemukan.')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def beranda(request):
    # Data petani per bulan
    petani_per_bulan = [Petani.objects.filter(created_at__month=bulan).count() for bulan in range(1, 13)]

    # Data lahan per bulan
    lahan_per_bulan = [Lahan.objects.filter(created_at__month=bulan).count() for bulan in range(1, 13)]

    # Total kebutuhan pupuk
    total_urea = DataERDKK.objects.aggregate(total=Sum('pupuk_urea'))['total'] or 0
    total_npk = DataERDKK.objects.aggregate(total=Sum('pupuk_npk'))['total'] or 0
    total_organik = DataERDKK.objects.aggregate(total=Sum('pupuk_organik'))['total'] or 0

    # Data terbaru
    anggota_terbaru = Petani.objects.order_by('-created_at')[:5]
    lahan_terbaru = Lahan.objects.order_by('-created_at')[:5]
    alsintan_terbaru = Alsintan.objects.order_by('-tanggal_pengadaan')[:5]

    context = {
        "judul": "Halaman Petani",
        "menu": "beranda", 
        'petani_per_bulan': petani_per_bulan,
        'lahan_per_bulan': lahan_per_bulan,
        'urea': total_urea,
        'npk': total_npk,
        'organik': total_organik,
        'anggota_terbaru': anggota_terbaru,
        'lahan_terbaru': lahan_terbaru,
        'alsintan_terbaru': alsintan_terbaru,
    }
    return render(request, 'beranda.html', context)

@login_required(login_url='login')
def profil(request):
    profil = ProfilGapoktan.objects.last()
    latest_kegiatan = Kegiatan.objects.order_by('-tanggal').first()  # Ambil 1 kegiatan terbaru
    context = {
        "judul": "Profil Gapoktan",
        "profil": profil,
        "menu":"profil",
        'latest_kegiatan': latest_kegiatan,
    }
    return render(request, 'profil.html', context)

@login_required(login_url='login')
def kegiatan_list(request):
    kegiatan_list = Kegiatan.objects.all().order_by('-tanggal')  # urutkan dari yang terbaru
    context = {
        'kegiatan_list': kegiatan_list,
        "menu":"profil",
    }
    return render(request, 'kegiatan_list.html', context)

@login_required(login_url='login')
def profil_kantor(request):
    profil = ProfilGapoktan.objects.last()
    return render(request, 'profil_kantor.html', {'profil': profil})

@login_required(login_url='login')
def profil_ketua(request):
    profil = ProfilGapoktan.objects.last()
    return render(request, 'profil_ketua.html', {'profil': profil})

@login_required(login_url='login')
def grup(request):
    query = request.GET.get('q')
    if query:
        query_grup = Grup.objects.filter(Q(nama__icontains=query)).order_by('-id')
    else:
        query_grup = Grup.objects.order_by('-id')

    context = {
        "judul": "Halaman grup",
        "menu":"grup",
        'grup': query_grup,
    }
    return render(request, 'grup.html', context)

@login_required(login_url='login')
def ketua(request):
    query = request.GET.get('q')
    if query:
        poktan = KetuaPoktan.objects.filter(
            Q(nama__icontains=query) | Q(grup__nama__icontains=query)
        ).order_by('-id').distinct()
        gapoktan = KetuaGapoktan.objects.filter(
            Q(nama__icontains=query) | Q(grup__nama__icontains=query)
        ).order_by('-id').distinct()
    else:
        poktan = KetuaPoktan.objects.order_by('-id')
        gapoktan = KetuaGapoktan.objects.order_by('-id')

    context = {
        'judul': 'Halaman Ketua',
        'menu': 'ketua',
        'poktan': poktan,
        'gapoktan': gapoktan,
    }
    return render(request, 'ketua.html', context)


@login_required(login_url='login')
def anggota(request):
    query = request.GET.get('q')
    if query:
        query_petani = Petani.objects.filter(
            Q(nama__icontains=query) | Q(grup__nama__icontains=query)
        ).order_by('-id')
    else:
        query_petani = Petani.objects.order_by('-id')
        
    paginator = Paginator(query_petani, 10)  # 10 data per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "judul": "Halaman anggota",
        "menu": "anggota",
        'petani': page_obj,
    }
    return render(request, 'anggota.html', context)

@login_required(login_url='login')
def alsintan(request):
    daftar_alsintan = Alsintan.objects.select_related('user').all().order_by('-id')
    context = {
        "judul": "Halaman Alsintan",
        "menu": "alsintan",
        "daftar_alsintan": daftar_alsintan,
        
    }
    return render(request, 'alsintan.html', context)

@login_required(login_url='login')
def tambah_alsintan(request):
    if request.method == 'POST':
        nama_alat = request.POST.get('nama_alat')
        pemilik = request.POST.get('pemilik')
        jumlah = request.POST.get('jumlah')
        kondisi = request.POST.get('kondisi')
        tanggal_pengadaan = request.POST.get('tanggal_pengadaan')
        sumber_dana = request.POST.get('sumber_dana')
        dokumentasi = request.FILES.get('dokumentasi')
        keterangan = request.POST.get('keterangan')

        if not nama_alat or not pemilik or not jumlah or not tanggal_pengadaan:
            messages.error(request, "Data tidak lengkap.")
            return redirect('alsintan')

        Alsintan.objects.create(
            nama_alat=nama_alat,
            pemilik=pemilik,
            jumlah=jumlah,
            kondisi=kondisi,
            tanggal_pengadaan=tanggal_pengadaan,
            sumber_dana=sumber_dana,
            dokumentasi=dokumentasi,
            keterangan=keterangan,
            user=request.user
        )
        messages.success(request, "Data Alsintan berhasil ditambahkan.")
        return redirect('alsintan')

    return redirect('alsintan')

@login_required(login_url='login')
def edit_alsintan(request, id):
    alsintan = get_object_or_404(Alsintan, pk=id)
    
    if alsintan.user != request.user:  # 👈 hanya pemilik yang bisa edit
        return HttpResponseForbidden("Kamu tidak bisa mengedit data ini.")
    
    if request.method == "POST":
        alsintan.nama_alat = request.POST.get("nama_alat")
        alsintan.jumlah = request.POST.get("jumlah")
        alsintan.kondisi = request.POST.get("kondisi")
        alsintan.tanggal_pengadaan = request.POST.get("tanggal_pengadaan")
        alsintan.sumber_dana = request.POST.get("sumber_dana")
        alsintan.keterangan = request.POST.get("keterangan")
        if request.FILES.get("dokumentasi"):
            alsintan.dokumentasi = request.FILES["dokumentasi"]
        alsintan.save()
    return redirect('alsintan')

@login_required(login_url='login')
def hapus_alsintan(request, id):
    alsintan = get_object_or_404(Alsintan, pk=id)
    
    if alsintan.user != request.user:  # 👈 hanya pemilik yang bisa hapus
        return HttpResponseForbidden("Kamu tidak bisa menghapus data ini.")
    
    alsintan.delete()
    return redirect('alsintan')


@login_required(login_url='login')
def lahan(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status_filter')

    if query:
        query_lahan = Lahan.objects.filter(
            Q(pemilik__nama__icontains=query) |
            Q(jenis_tanaman__icontains=query) |
            Q(lokasi__icontains=query)
        ).order_by('-id')
    else:
        query_lahan = Lahan.objects.order_by('-id')

    # Tambahan: Filter berdasarkan status
    status = request.GET.get('status_filter')
    if status:
        query_lahan = query_lahan.filter(status_panen=status)


    # Data untuk Google Maps
    lahan_data = [
        {
            'pemilik': l.pemilik.nama,
            'luas': l.luas,
            'jenis_tanaman': l.jenis_tanaman,
            'latitude': l.latitude,
            'longitude': l.longitude
        } for l in query_lahan if l.latitude and l.longitude
    ]

    lahan_edit_data = [
        {
            'id': l.id,
            'pemilik_id': l.pemilik.id,
            'luas': l.luas,
            'jenis_tanaman': l.jenis_tanaman,
            'lokasi': l.lokasi,
            'latitude': l.latitude,
            'longitude': l.longitude,
            'tanggal_tanam': l.tanggal_tanam.strftime('%Y-%m-%d') if l.tanggal_tanam else '',
            'tanggal_panen': l.tanggal_panen.strftime('%Y-%m-%d') if l.tanggal_panen else '',
        } for l in query_lahan
    ]

    context = {
        'judul': 'Halaman Lahan',
        "menu": "lahan",
        'lahan': query_lahan,
        'daftar_petani': Petani.objects.all(),
        'lahan_json': json.dumps(lahan_data, cls=DjangoJSONEncoder),
        'lahan_edit_json': json.dumps(lahan_edit_data, cls=DjangoJSONEncoder), 
    }
    return render(request, 'lahan.html', context)

@login_required
def edit_lahan(request, id):
    lahan = get_object_or_404(Lahan, id=id)
    
    if lahan.user != request.user:
        return HttpResponseForbidden("Kamu tidak bisa mengedit data ini.")

    if request.method == 'POST':
        lahan.pemilik_id = request.POST.get('pemilik')
        lahan.luas = request.POST.get('luas')
        lahan.jenis_tanaman = request.POST.get('jenis_tanaman')
        lahan.lokasi = request.POST.get('lokasi')
        lahan.latitude = request.POST.get('latitude')
        lahan.longitude = request.POST.get('longitude')
        lahan.tanggal_tanam = request.POST.get('tanggal_tanam')
        lahan.tanggal_panen = request.POST.get('tanggal_panen')
        status_panen = request.POST.get('status_panen', 'proses')
        lahan.status_panen = status_panen

        if request.FILES.get('gambar'):
            lahan.gambar_lahan = request.FILES['gambar']

        lahan.save()
        messages.success(request, 'Data lahan berhasil diperbarui.')
        return redirect('lahan')  # ganti dengan nama url halaman daftar lahan kamu

    return redirect('lahan')  # fallback jika bukan POST


@login_required
def tambah_lahan(request):
    if request.method == 'POST':
        gambar = request.FILES.get('gambar')
        pemilik_id = request.POST.get('pemilik')
        luas = request.POST.get('luas')
        jenis_tanaman = request.POST.get('jenis_tanaman')
        lokasi = request.POST.get('lokasi')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        tanggal_tanam = request.POST.get('tanggal_tanam')
        tanggal_panen = request.POST.get('tanggal_panen')
        status_panen = request.POST.get('status_panen', 'proses') 

        try:
            pemilik_obj = Petani.objects.get(id=pemilik_id)
        except Petani.DoesNotExist:
            return HttpResponse("Pemilik tidak ditemukan", status=400)
        
        if Lahan.objects.filter(pemilik=pemilik_obj).exists():
            messages.error(request, "Petani ini sudah memiliki lahan.")
            return redirect('tambah_lahan')
        
        Lahan.objects.create(
            gambar_lahan=gambar,
            pemilik=pemilik_obj,
            luas=luas,
            jenis_tanaman=jenis_tanaman,
            lokasi=lokasi,
            latitude=latitude,
            longitude=longitude,
            tanggal_tanam=tanggal_tanam,
            tanggal_panen=tanggal_panen,
            status_panen=status_panen,
            user=request.user
        )
        return redirect('lahan')

    return redirect('lahan')

@login_required(login_url='login')
def erdkk(request):
    daftar_erdkk = DataERDKK.objects.all().order_by('-tahun_rencana')
    daftar_pengajuan = Sppt.objects.filter(user=request.user).order_by('-tanggal_pengajuan')
    context = {
        'judul': 'Data ERDKK',
        "menu": "erdkk",
        'daftar_erdkk': daftar_erdkk,
        'daftar_pengajuan': daftar_pengajuan,
    }
    return render(request, 'erdkk.html', context)

@login_required(login_url='login')
def ajukan_sppt(request):
    if request.method == 'POST':
        nama_petani = request.POST.get('nama_petani')
        nama_ibu = request.POST.get('nama_ibu')

        fotokopi_ktp = request.FILES.get('fotokopi_ktp')
        fotokopi_kk = request.FILES.get('fotokopi_kk')
        fotokopi_sppt = request.FILES.get('fotokopi_sppt')

        if not all([nama_petani, nama_ibu, fotokopi_ktp, fotokopi_kk, fotokopi_sppt]):
            messages.error(request, "Semua field wajib diisi.")
            return redirect('erdkk')

        # Optional: cek duplikat berdasarkan nama_petani (kalau perlu)
        if Sppt.objects.filter(nama_petani=nama_petani).exists():
            messages.error(request, "Petani ini sudah mengajukan SPPT.")
            return redirect('erdkk')

        sppt = Sppt.objects.create(
            nama_petani=nama_petani,
            nama_ibu=nama_ibu,
            fotokopi_ktp=fotokopi_ktp,
            fotokopi_kk=fotokopi_kk,
            fotokopi_sppt=fotokopi_sppt,
            user=request.user
        )

        messages.success(request, "Pengajuan SPPT berhasil dikirim.")
        return redirect('erdkk')

    return redirect('erdkk')

@login_required(login_url='login')
def tanaman(request):
    query_tanaman = PenyakitTanaman.objects.order_by('-id')
    context = {
        "judul": "Halaman Tanaman",
        "menu": "tanaman",
        'tanaman': query_tanaman,
    }
    return render(request, 'tanaman.html', context)

# Form untuk ForumDiskusi dan KomentarDiskusi
class ForumDiskusiForm(forms.ModelForm):
    class Meta:
        model = ForumDiskusi
        fields = ['judul', 'isi']

class KomentarDiskusiForm(forms.ModelForm):
    class Meta:
        model = KomentarDiskusi
        fields = ['isi']

# Views
@login_required(login_url='login')
def daftar_forum(request):
    forum_list = ForumDiskusi.objects.all().order_by('-tanggal')
    context = {
        'forum_list': forum_list,
        "menu": "forum",
    }
    return render(request, 'daftar_forum.html', context)

@login_required(login_url='login')
def detail_forum(request, forum_id):
    forum = get_object_or_404(ForumDiskusi, id=forum_id)
    komentar_list = forum.komentar.all().order_by('tanggal')

    if request.method == 'POST':
        form_komentar = KomentarDiskusiForm(request.POST)
        if form_komentar.is_valid():
            komentar = form_komentar.save(commit=False)
            komentar.user = request.user
            komentar.forum = forum
            komentar.tanggal = timezone.now()
            komentar.save()
            return redirect('detail_forum', forum_id=forum.id)
    else:
        form_komentar = KomentarDiskusiForm()

    context = {
        'forum': forum,
        'komentar_list': komentar_list,
        'form_komentar': form_komentar,
    }
    return render(request, 'detail_forum.html', context)

@login_required(login_url='login')
def buat_forum(request):
    if request.method == 'POST':
        form = ForumDiskusiForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.user = request.user
            forum.tanggal = timezone.now()
            forum.save()
            return redirect('daftar_forum')
    else:
        form = ForumDiskusiForm()

    return render(request, 'buat_forum.html', {'form': form})

@login_required(login_url='login')
def hapus_forum(request, pk):
    forum = get_object_or_404(ForumDiskusi, pk=pk)
    if forum.user != request.user:
        return HttpResponseForbidden("Anda tidak punya izin menghapus diskusi ini.")
    if request.method == 'POST':
        forum.delete()
        return redirect('daftar_forum')
    # Kalau mau buat konfirmasi via halaman terpisah, bisa ditambahkan.
    return redirect('detail_forum', forum_id=pk)

@login_required(login_url='login')
def hapus_komentar(request, pk):
    komentar = get_object_or_404(KomentarDiskusi, pk=pk)
    if komentar.user != request.user:
        return HttpResponseForbidden("Anda tidak punya izin menghapus komentar ini.")
    
    forum_id = komentar.forum.id  # Simpan dulu sebelum dihapus
    
    if request.method == 'POST':
        komentar.delete()
    
    return redirect('detail_forum', forum_id=forum_id)  # ← gunakan forum_id, bukan pk


def logoutPage(request):
    logout(request)
    return redirect('login')