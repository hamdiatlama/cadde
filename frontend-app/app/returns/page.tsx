'use client';
import { useState } from 'react';

const myReturns = [
  { id: 'RET-2026-001', order: 'ORD-2026-0421', product: 'Basic T-Shirt Kırmızı/M', reason: 'Beden uymadı', status: 'approved', date: '2026-06-10', amount: 149 },
  { id: 'RET-2026-002', order: 'ORD-2026-0418', product: 'Slim Fit Pantolon Mavi/L', reason: 'Ürün hasarlı', status: 'pending', date: '2026-06-13', amount: 299 },
  { id: 'RET-2026-003', order: 'ORD-2026-0415', product: 'Kazak Yeşil/XL', reason: 'Renk farklı geldi', status: 'completed', date: '2026-06-05', amount: 199 },
];

const statusLabels: Record<string, { label: string; style: string }> = {
  pending: { label: 'İnceleniyor', style: 'bg-yellow-100 text-yellow-800' },
  approved: { label: 'Onaylandı', style: 'bg-green-100 text-green-800' },
  completed: { label: 'Tamamlandı', style: 'bg-blue-100 text-blue-800' },
  rejected: { label: 'Reddedildi', style: 'bg-red-100 text-red-800' },
};

export default function ReturnsPage() {
  const [tab, setTab] = useState<'list' | 'create'>('list');
  const [reason, setReason] = useState('');
  const [orderId, setOrderId] = useState('');

  function handleCreate() {
    if (orderId && reason) {
      alert('İade talebi oluşturuldu!');
      setOrderId('');
      setReason('');
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">İade İşlemleri</h1>
      <p className="text-gray-500 mb-6">Ürün iade taleplerinizi yönetin ve takip edin</p>

      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-blue-700">{myReturns.length}</p>
          <p className="text-sm text-gray-600">Toplam İade</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-700">{myReturns.filter(r => r.status === 'pending').length}</p>
          <p className="text-sm text-gray-600">Bekleyen</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-green-700">{myReturns.filter(r => r.status === 'approved' || r.status === 'completed').length}</p>
          <p className="text-sm text-gray-600">Sonuçlanan</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6">
        {(['list', 'create'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'list' ? 'İadelerim' : 'İade Oluştur'}
          </button>
        ))}
      </div>

      {tab === 'create' && (
        <div className="border rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">Yeni İade Talebi</h2>
          <div className="grid gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Sipariş Numarası</label>
              <input value={orderId} onChange={e => setOrderId(e.target.value)}
                placeholder="Örn: ORD-2026-XXXX" className="border p-2 rounded w-full text-sm" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">İade Nedeni</label>
              <select value={reason} onChange={e => setReason(e.target.value)} className="border p-2 rounded w-full text-sm">
                <option value="">Seçiniz</option>
                <option value="Beden uymadı">Beden uymadı</option>
                <option value="Ürün hasarlı">Ürün hasarlı</option>
                <option value="Renk farklı geldi">Renk farklı geldi</option>
                <option value="Yanlış ürün gönderildi">Yanlış ürün gönderildi</option>
                <option value="Diğer">Diğer</option>
              </select>
            </div>
            <button onClick={handleCreate} disabled={!orderId || !reason}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
              İade Talebi Oluştur
            </button>
          </div>
        </div>
      )}

      {tab === 'list' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">İade No</th>
                <th className="text-left p-3 text-sm font-semibold">Sipariş</th>
                <th className="text-left p-3 text-sm font-semibold">Ürün</th>
                <th className="text-left p-3 text-sm font-semibold">Neden</th>
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-right p-3 text-sm font-semibold">Tutar</th>
                <th className="text-left p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {myReturns.map(r => (
                <tr key={r.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-mono">{r.id}</td>
                  <td className="p-3 text-sm">{r.order}</td>
                  <td className="p-3 text-sm">{r.product}</td>
                  <td className="p-3 text-sm">{r.reason}</td>
                  <td className="p-3 text-sm">{r.date}</td>
                  <td className="p-3 text-sm text-right font-semibold">{r.amount} TL</td>
                  <td className="p-3 text-sm">
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold ${statusLabels[r.status].style}`}>
                      {statusLabels[r.status].label}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
