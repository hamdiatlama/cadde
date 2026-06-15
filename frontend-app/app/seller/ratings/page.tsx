'use client';
import { useState } from 'react';

const badges = [
  { name: 'Hızlı Gönderim', icon: '🚀', desc: 'Siparişleri 24 saat içinde gönder', earned: true },
  { name: 'Güvenilir Satıcı', icon: '✅', desc: '100+ olumlu yorum', earned: true },
  { name: 'Premium Üye', icon: '⭐', desc: 'Aktif üyelik süresi 1 yıl', earned: true },
  { name: 'Toplu Satış Ustası', icon: '📦', desc: '50+ toplu sipariş', earned: false },
  { name: 'Yıldız İletişim', icon: '💬', desc: 'Mesajlara 1 saat içinde dönüş', earned: false },
  { name: 'Sezonun En İyisi', icon: '🏆', desc: 'Aylık en yüksek satış', earned: false },
];

const reviews = [
  { id: 1, user: 'Ahmet K.', rating: 5, text: 'Ürün çok hızlı geldi, teşekkürler!', date: '2 gün önce' },
  { id: 2, user: 'Fatma S.', rating: 5, text: 'Kaliteli ürün, güvenilir satıcı.', date: '1 hafta önce' },
  { id: 3, user: 'Mustafa T.', rating: 4, text: 'Beklediğim gibi çıktı, teşekkürler.', date: '2 hafta önce' },
  { id: 4, user: 'Zeynep A.', rating: 3, text: 'Ürün güzel ama kargo biraz geç geldi.', date: '3 hafta önce' },
  { id: 5, user: 'Ali R.', rating: 5, text: 'Her şey mükemmeldi, tekrar sipariş vereceğim.', date: '1 ay önce' },
];

export default function SellerRatingsPage() {
  const [activeTab, setActiveTab] = useState<'genel' | 'yorumlar' | 'rozetler'>('genel');

  const avgRating = (reviews.reduce((a, r) => a + r.rating, 0) / reviews.length).toFixed(1);
  const ratingCounts = [0, 0, 0, 0, 0];
  reviews.forEach(r => ratingCounts[r.rating - 1]++);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Satıcı Puanları ve Rozetler</h1>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setActiveTab('genel')} className={`px-4 py-2 rounded-lg text-sm font-semibold ${activeTab === 'genel' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Genel</button>
        <button onClick={() => setActiveTab('yorumlar')} className={`px-4 py-2 rounded-lg text-sm font-semibold ${activeTab === 'yorumlar' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Yorumlar</button>
        <button onClick={() => setActiveTab('rozetler')} className={`px-4 py-2 rounded-lg text-sm font-semibold ${activeTab === 'rozetler' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Rozetler</button>
      </div>

      {activeTab === 'genel' && (
        <>
          <div className="grid gap-4 md:grid-cols-4 mb-8">
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-3xl font-bold text-blue-700">{avgRating}</p>
              <p className="text-sm text-gray-600">Ortalama Puan</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg text-center">
              <p className="text-3xl font-bold text-green-700">{reviews.length}</p>
              <p className="text-sm text-gray-600">Toplam Yorum</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg text-center">
              <p className="text-3xl font-bold text-purple-700">{badges.filter(b => b.earned).length}</p>
              <p className="text-sm text-gray-600">Kazanılan Rozet</p>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg text-center">
              <p className="text-3xl font-bold text-yellow-700">%{Math.round((reviews.filter(r => r.rating >= 4).length / reviews.length) * 100)}</p>
              <p className="text-sm text-gray-600">Memnuniyet Oranı</p>
            </div>
          </div>

          <div className="border rounded-lg p-5">
            <h3 className="font-semibold mb-4">Puan Dağılımı</h3>
            {[5, 4, 3, 2, 1].map(star => {
              const count = ratingCounts[star - 1];
              const pct = reviews.length > 0 ? (count / reviews.length) * 100 : 0;
              return (
                <div key={star} className="flex items-center gap-3 mb-2">
                  <span className="text-sm w-8">{star} ★</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                    <div className="bg-yellow-400 rounded-full h-3" style={{ width: `${pct}%` }}></div>
                  </div>
                  <span className="text-sm text-gray-500 w-8">{count}</span>
                </div>
              );
            })}
          </div>
        </>
      )}

      {activeTab === 'yorumlar' && (
        <div className="space-y-3">
          {reviews.map(r => (
            <div key={r.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-sm font-semibold text-blue-700">{r.user[0]}</div>
                  <span className="font-semibold text-sm">{r.user}</span>
                </div>
                <span className="text-yellow-500 text-sm">{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span>
              </div>
              <p className="text-sm text-gray-600">{r.text}</p>
              <p className="text-xs text-gray-400 mt-1">{r.date}</p>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'rozetler' && (
        <div className="grid gap-4 md:grid-cols-3">
          {badges.map(b => (
            <div key={b.name} className={`border rounded-lg p-5 ${b.earned ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200 opacity-60'}`}>
              <div className="text-3xl mb-2">{b.icon}</div>
              <h3 className="font-semibold">{b.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{b.desc}</p>
              <span className={`inline-block mt-3 text-xs font-semibold px-2 py-0.5 rounded ${b.earned ? 'bg-green-200 text-green-800' : 'bg-gray-200 text-gray-600'}`}>
                {b.earned ? 'Kazanıldı' : 'Kazanılmadı'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
