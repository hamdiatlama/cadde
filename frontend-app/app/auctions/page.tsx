'use client';
import { useState } from 'react';

const auctions = [
  { id: 1, title: 'Vintage Deri Ceket', currentBid: 1250, startingBid: 500, endTime: '2026-06-16 18:00', bidCount: 23, image: null },
  { id: 2, title: 'El Yapımı Seramik Vazo', currentBid: 340, startingBid: 100, endTime: '2026-06-15 20:00', bidCount: 8, image: null },
  { id: 3, title: 'Antika Gümüş Saat', currentBid: 2800, startingBid: 1000, endTime: '2026-06-17 12:00', bidCount: 15, image: null },
  { id: 4, title: 'Koleksiyonluk Pul Seti', currentBid: 420, startingBid: 200, endTime: '2026-06-18 15:00', bidCount: 5, image: null },
  { id: 5, title: 'Resim Elmas Baskı Tablo', currentBid: 1890, startingBid: 700, endTime: '2026-06-16 22:00', bidCount: 31, image: null },
  { id: 6, title: 'Nadir Plak Koleksiyonu', currentBid: 950, startingBid: 300, endTime: '2026-06-19 10:00', bidCount: 12, image: null },
];

function getTimeRemaining(endTime: string) {
  const diff = new Date(endTime).getTime() - Date.now();
  if (diff <= 0) return 'Sona erdi';
  const h = Math.floor(diff / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  return `${h}s ${m}d`;
}

export default function AuctionsPage() {
  const [filter, setFilter] = useState<'all' | 'active' | 'ending'>('active');

  const filtered = auctions.filter(a => {
    if (filter === 'active') return new Date(a.endTime).getTime() > Date.now();
    if (filter === 'ending') {
      const diff = new Date(a.endTime).getTime() - Date.now();
      return diff > 0 && diff < 86400000;
    }
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Aktif Açık Artırmalar</h1>
      <p className="text-gray-500 mb-6">Canlı tekliflerle en iyi fırsatları yakalayın</p>

      <div className="flex gap-2 mb-6">
        {(['active', 'ending', 'all'] as const).map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {f === 'active' ? 'Aktif' : f === 'ending' ? 'Bitişine Az Kaldı' : 'Tümü'}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map(a => {
          const ended = new Date(a.endTime).getTime() <= Date.now();
          const remaining = getTimeRemaining(a.endTime);
          return (
            <div key={a.id} className={`border rounded-lg p-5 shadow-sm hover:shadow-md ${ended ? 'opacity-50' : ''}`}>
              <div className="h-32 bg-gradient-to-br from-blue-50 to-purple-50 rounded mb-4 flex items-center justify-center text-gray-400 text-sm">
                {a.image || 'Ürün Görseli'}
              </div>
              <h2 className="font-semibold text-lg mb-2">{a.title}</h2>
              <div className="flex justify-between items-center mb-3">
                <div>
                  <p className="text-sm text-gray-500">Güncel Teklif</p>
                  <p className="text-xl font-bold text-blue-700">{a.currentBid.toLocaleString()} TL</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">{ended ? 'Bitiş' : 'Kalan'}</p>
                  <p className={`text-sm font-semibold ${ended ? 'text-red-500' : 'text-green-600'}`}>{remaining}</p>
                </div>
              </div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs text-gray-400">{a.bidCount} teklif</span>
                <span className="text-xs text-gray-400">Başlangıç: {a.startingBid} TL</span>
              </div>
              <button disabled={ended}
                className={`w-full py-2 rounded-lg text-sm font-semibold ${ended ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-blue-600 text-white hover:bg-blue-700'}`}>
                {ended ? 'Sona Erdi' : 'Teklif Ver'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
