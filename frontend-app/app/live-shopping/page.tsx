'use client';
import { useState } from 'react';

const streams = [
  { id: 1, title: 'Yaz Koleksiyonu Tanıtımı', host: 'Elif Hanım', status: 'live', viewers: 1240, startTime: '2026-06-15 14:00', category: 'Moda' },
  { id: 2, title: 'Mutfak Gereçleri Canlı Gösterim', host: 'Ahmet Usta', status: 'live', viewers: 876, startTime: '2026-06-15 15:30', category: 'Ev & Yaşam' },
  { id: 3, title: 'Teknoloji Fırsatları', host: 'Can Teknik', status: 'scheduled', viewers: 0, startTime: '2026-06-16 11:00', category: 'Teknoloji' },
  { id: 4, title: 'El Yapımı Takı Atölyesi', host: 'Zeynep Tasarım', status: 'scheduled', viewers: 0, startTime: '2026-06-17 14:00', category: 'Aksesuar' },
  { id: 5, title: 'Spor Giyim Sezon İndirimi', host: 'Ali Spor', status: 'live', viewers: 2105, startTime: '2026-06-15 13:00', category: 'Spor' },
  { id: 6, title: 'Organik Ürünler Tadım Günü', host: 'Doğal Köy', status: 'scheduled', viewers: 0, startTime: '2026-06-18 10:00', category: 'Gıda' },
];

export default function LiveShoppingPage() {
  const [filter, setFilter] = useState<'live' | 'scheduled'>('live');

  const filtered = streams.filter(s => s.status === filter);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Canlı Alışveriş</h1>
      <p className="text-gray-500 mb-6">Canlı yayınlarla ürünleri yakından keşfedin, anında satın alın</p>

      <div className="flex gap-2 mb-6">
        {(['live', 'scheduled'] as const).map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {f === 'live' ? 'Canlı Yayınlar' : 'Planlanan Yayınlar'}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map(s => (
          <div key={s.id} className="border rounded-lg shadow-sm hover:shadow-md overflow-hidden">
            <div className={`h-40 flex items-center justify-center relative ${s.status === 'live' ? 'bg-gradient-to-br from-red-50 to-orange-50' : 'bg-gradient-to-br from-gray-50 to-blue-50'}`}>
              <span className="text-4xl text-gray-300">{s.status === 'live' ? '▶' : '📅'}</span>
              {s.status === 'live' && (
                <span className="absolute top-3 left-3 bg-red-600 text-white text-xs px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                  CANLI
                </span>
              )}
              <span className="absolute top-3 right-3 bg-black/60 text-white text-xs px-2 py-0.5 rounded">
                {s.category}
              </span>
            </div>
            <div className="p-4">
              <h2 className="font-semibold text-lg mb-1">{s.title}</h2>
              <p className="text-sm text-gray-500 mb-2">Sunucu: {s.host}</p>
              <div className="flex items-center justify-between">
                <div className="text-sm">
                  {s.status === 'live' ? (
                    <span className="text-green-600 font-semibold">{s.viewers.toLocaleString()} izleyici</span>
                  ) : (
                    <span className="text-gray-500">{new Date(s.startTime).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })}</span>
                  )}
                </div>
                <button className={`px-3 py-1.5 rounded text-sm font-semibold ${s.status === 'live' ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-blue-600 text-white hover:bg-blue-700'}`}>
                  {s.status === 'live' ? 'İzle' : 'Hatırlat'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
