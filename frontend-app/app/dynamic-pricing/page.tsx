'use client';
import { useState } from 'react';

const pricingRules = [
  { id: 1, name: 'Sezon İndirimi - Yaz', type: 'percentage', value: 15, condition: 'Kategori: Giyim', status: 'active', priority: 1 },
  { id: 2, name: 'Stok Fazlası İndirimi', type: 'percentage', value: 30, condition: 'Stok > 50 adet', status: 'active', priority: 2 },
  { id: 3, name: 'VIP Müşteri İndirimi', type: 'percentage', value: 10, condition: 'Müşteri segmenti: VIP', status: 'active', priority: 3 },
  { id: 4, name: 'Sepet Tutarı İndirimi', type: 'fixed', value: 50, condition: 'Sepet > 500 TL', status: 'inactive', priority: 4 },
  { id: 5, name: 'Yeni Ürün Lansman', type: 'percentage', value: 5, condition: 'Yeni eklenen ürünler (30 gün)', status: 'active', priority: 5 },
  { id: 6, name: 'Toptan Alım İndirimi', type: 'percentage', value: 20, condition: 'Adet >= 10', status: 'inactive', priority: 6 },
  { id: 7, name: 'Saatlik Fırsat', type: 'fixed', value: 25, condition: 'Saat 14:00 - 16:00 arası', status: 'active', priority: 7 },
];

const timeSlots = [
  { day: 'Pazartesi', multiplier: 1.0 },
  { day: 'Salı', multiplier: 1.0 },
  { day: 'Çarşamba', multiplier: 1.0 },
  { day: 'Perşembe', multiplier: 1.0 },
  { day: 'Cuma', multiplier: 1.2 },
  { day: 'Cumartesi', multiplier: 1.3 },
  { day: 'Pazar', multiplier: 1.1 },
];

export default function DynamicPricingPage() {
  const [tab, setTab] = useState<'rules' | 'schedule'>('rules');
  const [rules, setRules] = useState(pricingRules);

  const toggleStatus = (id: number) => {
    setRules(prev => prev.map(r => r.id === id ? { ...r, status: r.status === 'active' ? 'inactive' : 'active' } : r));
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Dinamik Fiyatlama</h1>
      <p className="text-gray-500 mb-6">Otomatik fiyatlandırma kurallarını yönetin</p>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('rules')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'rules' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Fiyat Kuralları</button>
        <button onClick={() => setTab('schedule')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'schedule' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Zaman Çizelgesi</button>
      </div>

      {tab === 'rules' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Kural</th>
                <th className="text-left p-3 text-sm font-semibold">İndirim</th>
                <th className="text-left p-3 text-sm font-semibold">Koşul</th>
                <th className="text-center p-3 text-sm font-semibold">Öncelik</th>
                <th className="text-center p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {rules.map(r => (
                <tr key={r.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-semibold">{r.name}</td>
                  <td className="p-3 text-sm">
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${r.type === 'percentage' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                      {r.type === 'percentage' ? `%${r.value}` : `${r.value} TL`}
                    </span>
                  </td>
                  <td className="p-3 text-sm text-gray-600">{r.condition}</td>
                  <td className="p-3 text-sm text-center">{r.priority}</td>
                  <td className="p-3 text-center">
                    <button onClick={() => toggleStatus(r.id)}
                      className={`text-xs px-2 py-1 rounded font-semibold ${r.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                      {r.status === 'active' ? 'Aktif' : 'Pasif'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'schedule' && (
        <div className="border rounded-lg overflow-hidden">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Gün</th>
                <th className="text-left p-3 text-sm font-semibold">Çarpan</th>
                <th className="text-left p-3 text-sm font-semibold">Açıklama</th>
              </tr>
            </thead>
            <tbody>
              {timeSlots.map(ts => (
                <tr key={ts.day} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-semibold">{ts.day}</td>
                  <td className="p-3 text-sm">
                    <span className={`font-bold ${ts.multiplier > 1.0 ? 'text-red-600' : 'text-green-600'}`}>
                      x{ts.multiplier.toFixed(1)}
                    </span>
                  </td>
                  <td className="p-3 text-sm text-gray-500">
                    {ts.multiplier > 1.0 ? `Fiyat %${Math.round((ts.multiplier - 1) * 100)} artırılır` : 'Standart fiyat'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <button className="mt-6 border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-lg p-4 w-full text-center text-sm text-gray-500 hover:text-blue-600 font-semibold transition-colors">
        + Yeni Kural Ekle
      </button>
    </div>
  );
}
