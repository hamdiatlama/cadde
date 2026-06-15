'use client';
import { useState } from 'react';

const myRequests = [
  { id: 1, title: 'Özel Desenli Seramik Kupa', category: 'El Sanatları', budget: 500, status: 'pending', date: '2026-06-14', offers: 3 },
  { id: 2, title: 'Kişiye Özel Ahşap Oyma Tablo', category: 'Dekorasyon', budget: 1200, status: 'in_progress', date: '2026-06-10', offers: 5 },
  { id: 3, title: 'El Yapımı Deri Cüzdan', category: 'Aksesuar', budget: 800, status: 'completed', date: '2026-05-28', offers: 7 },
  { id: 4, title: 'Özel Kesim Kadife Elbise', category: 'Giyim', budget: 1500, status: 'pending', date: '2026-06-13', offers: 2 },
];

const statusLabels: Record<string, { label: string; style: string }> = {
  pending: { label: 'Teklif Bekliyor', style: 'bg-yellow-100 text-yellow-800' },
  in_progress: { label: 'Çalışılıyor', style: 'bg-blue-100 text-blue-800' },
  completed: { label: 'Tamamlandı', style: 'bg-green-100 text-green-800' },
};

export default function CustomOrdersPage() {
  const [tab, setTab] = useState<'list' | 'create'>('list');
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [budget, setBudget] = useState(0);
  const [description, setDescription] = useState('');

  function handleCreate() {
    if (title && category && budget) {
      alert('Özel sipariş talebiniz oluşturuldu!');
      setTitle('');
      setCategory('');
      setBudget(0);
      setDescription('');
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Özel Sipariş</h1>
      <p className="text-gray-500 mb-6">El emeği, kişiye özel ürünleri ustalara sipariş verin</p>

      <div className="flex gap-2 mb-6">
        {(['list', 'create'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'list' ? 'Siparişlerim' : 'Yeni Sipariş'}
          </button>
        ))}
      </div>

      {tab === 'create' && (
        <div className="border rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">Yeni Özel Sipariş Talebi</h2>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Talep Başlığı</label>
              <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Ne yaptırmak istiyorsunuz?" className="border p-2 rounded w-full text-sm" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Kategori</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="border p-2 rounded w-full text-sm">
                <option value="">Seçiniz</option>
                <option value="El Sanatları">El Sanatları</option>
                <option value="Dekorasyon">Dekorasyon</option>
                <option value="Aksesuar">Aksesuar</option>
                <option value="Giyim">Giyim</option>
                <option value="Mobilya">Mobilya</option>
                <option value="Diğer">Diğer</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Bütçe (TL)</label>
              <input type="number" value={budget || ''} onChange={e => setBudget(Number(e.target.value))} placeholder="Maksimum bütçeniz" className="border p-2 rounded w-full text-sm" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Süre Tercihi</label>
              <select className="border p-2 rounded w-full text-sm">
                <option>1 hafta</option>
                <option>2 hafta</option>
                <option>1 ay</option>
                <option>Esnek</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm text-gray-600 mb-1">Detaylı Açıklama</label>
              <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3} placeholder="Ürünle ilgili detayları, ölçüleri, renk tercihlerinizi belirtin..." className="border p-2 rounded w-full text-sm" />
            </div>
            <div className="md:col-span-2">
              <button onClick={handleCreate} disabled={!title || !category || !budget}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
                Talebi Gönder
              </button>
            </div>
          </div>
        </div>
      )}

      {tab === 'list' && (
        <div className="grid gap-4">
          {myRequests.map(r => (
            <div key={r.id} className="border rounded-lg p-4 hover:shadow-md">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-semibold">{r.title}</h3>
                  <p className="text-sm text-gray-500">{r.category}</p>
                </div>
                <span className={`px-2 py-0.5 rounded text-xs font-semibold ${statusLabels[r.status].style}`}>
                  {statusLabels[r.status].label}
                </span>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>Bütçe: <strong>{r.budget.toLocaleString()} TL</strong></span>
                <span>{r.offers} teklif</span>
                <span>{r.date}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
