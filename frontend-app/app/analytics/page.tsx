'use client';
import { useState } from 'react';

const summaryCards = [
  { label: 'Toplam Satış (Bu Ay)', value: '₺284.500', change: '+12%', positive: true },
  { label: 'Toplam Sipariş', value: '1.842', change: '+8%', positive: true },
  { label: 'Dönüşüm Oranı', value: '%3,2', change: '+0.4%', positive: true },
  { label: 'Ortalama Sepet', value: '₺154,50', change: '-2%', positive: false },
  { label: ' aktif Ürün', value: '4.230', change: '+124', positive: true },
  { label: 'Toplam Ziyaretçi', value: '58.340', change: '+23%', positive: true },
];

const reports = [
  { id: 1, title: 'Satış Raporu', desc: 'Günlük/haftalık/aylık satış özeti', icon: '📊', category: 'sales' },
  { id: 2, title: 'Ürün Performansı', desc: 'En çok satan ürünler ve kategoriler', icon: '🏷️', category: 'products' },
  { id: 3, title: 'Müşteri Analizi', desc: 'Müşteri segmentasyonu ve davranışları', icon: '👥', category: 'customers' },
  { id: 4, title: 'Sepet Analizi', desc: 'Sepet terk oranları ve iyileştirme', icon: '🛒', category: 'sales' },
  { id: 5, title: 'Trafik Raporu', desc: 'Site trafiği ve kaynakları', icon: '🌐', category: 'traffic' },
  { id: 6, title: 'Kampanya ROI', desc: 'Kampanya performansı ve yatırım getirisi', icon: '📈', category: 'marketing' },
  { id: 7, title: 'Stok Raporu', desc: 'Stok seviyeleri ve yeniden sipariş noktaları', icon: '📦', category: 'products' },
  { id: 8, title: 'İade Analizi', desc: 'İade sebepleri ve oranları', icon: '↩️', category: 'sales' },
  { id: 9, title: 'Satıcı Performansı', desc: 'Satıcı bazlı satış ve puanlama', icon: '⭐', category: 'sellers' },
  { id: 10, title: 'Finansal Özet', desc: 'Gelir, gider ve kar analizi', icon: '💰', category: 'financial' },
  { id: 11, title: 'Pazar Yeri Karşılaştırma', desc: 'Rakip fiyat ve ürün analizi', icon: '🏪', category: 'market' },
  { id: 12, title: 'Mobil Uygulama', desc: 'Mobil kullanım istatistikleri', icon: '📱', category: 'traffic' },
];

const categories = [
  { id: 'all', label: 'Tümü' },
  { id: 'sales', label: 'Satış' },
  { id: 'products', label: 'Ürün' },
  { id: 'customers', label: 'Müşteri' },
  { id: 'traffic', label: 'Trafik' },
  { id: 'marketing', label: 'Pazarlama' },
  { id: 'financial', label: 'Finans' },
  { id: 'sellers', label: 'Satıcı' },
  { id: 'market', label: 'Pazar' },
];

export default function AnalyticsPage() {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? reports : reports.filter(r => r.category === filter);

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Analytics</h1>

      <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-6 mb-8">
        {summaryCards.map(c => (
          <div key={c.label} className="border rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">{c.label}</p>
            <p className="text-lg font-bold">{c.value}</p>
            <p className={`text-xs font-semibold ${c.positive ? 'text-green-600' : 'text-red-600'}`}>{c.change}</p>
          </div>
        ))}
      </div>

      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button key={cat.id} onClick={() => setFilter(cat.id)}
            className={`whitespace-nowrap px-3 py-1.5 rounded text-sm font-semibold ${filter === cat.id ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {cat.label}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map(r => (
          <div key={r.id} className="border rounded-lg p-5 hover:shadow-md transition-shadow cursor-pointer">
            <div className="text-2xl mb-2">{r.icon}</div>
            <h3 className="font-semibold">{r.title}</h3>
            <p className="text-sm text-gray-500 mt-1">{r.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
