'use client';
import { useState } from 'react';

const commissionTiers = [
  { category: 'Elektronik', rate: '3%', minFee: 5, maxFee: 500, example: '10.000 TL ürün → 300 TL komisyon' },
  { category: 'Moda & Giyim', rate: '5%', minFee: 3, maxFee: 200, example: '500 TL ürün → 25 TL komisyon' },
  { category: 'Ev & Yaşam', rate: '4%', minFee: 3, maxFee: 300, example: '1.000 TL ürün → 40 TL komisyon' },
  { category: 'Spor & Outdoor', rate: '4%', minFee: 3, maxFee: 300, example: '750 TL ürün → 30 TL komisyon' },
  { category: 'Kozmetik', rate: '6%', minFee: 3, maxFee: 150, example: '300 TL ürün → 18 TL komisyon' },
  { category: 'Gıda', rate: '2%', minFee: 1, maxFee: 100, example: '200 TL ürün → 4 TL komisyon' },
];

const commissionHistory = [
  { id: 1, date: '2026-06-14', product: 'Basic T-Shirt', saleAmount: 149, commission: 7.45, status: 'pending' },
  { id: 2, date: '2026-06-13', product: 'Slim Fit Pantolon', saleAmount: 299, commission: 14.95, status: 'cleared' },
  { id: 3, date: '2026-06-12', product: 'Kazak', saleAmount: 199, commission: 9.95, status: 'cleared' },
  { id: 4, date: '2026-06-10', product: 'Spor Ayakkabı', saleAmount: 399, commission: 15.96, status: 'cleared' },
  { id: 5, date: '2026-06-08', product: 'Bluetooth Kulaklık', saleAmount: 549, commission: 16.47, status: 'pending' },
  { id: 6, date: '2026-06-05', product: 'Deri Cüzdan', saleAmount: 89, commission: 4.45, status: 'cleared' },
];

const statusLabels: Record<string, string> = {
  pending: 'text-yellow-600 bg-yellow-50',
  cleared: 'text-green-600 bg-green-50',
};

export default function CommissionPage() {
  const [tab, setTab] = useState<'rates' | 'history'>('rates');

  const totalPending = commissionHistory.filter(h => h.status === 'pending').reduce((a, h) => a + h.commission, 0);
  const totalCleared = commissionHistory.filter(h => h.status === 'cleared').reduce((a, h) => a + h.commission, 0);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Komisyon Oranları</h1>
      <p className="text-gray-500 mb-6">Satıcı komisyon yapısı ve kazanç geçmişiniz</p>

      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-blue-700">{commissionHistory.length}</p>
          <p className="text-sm text-gray-600">Toplam İşlem</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-700">{totalPending.toFixed(2)} TL</p>
          <p className="text-sm text-gray-600">Bekleyen Komisyon</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-green-700">{totalCleared.toFixed(2)} TL</p>
          <p className="text-sm text-gray-600">Ödenen Komisyon</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6">
        {(['rates', 'history'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'rates' ? 'Komisyon Tablosu' : 'Komisyon Geçmişi'}
          </button>
        ))}
      </div>

      {tab === 'rates' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Kategori</th>
                <th className="text-left p-3 text-sm font-semibold">Komisyon Oranı</th>
                <th className="text-left p-3 text-sm font-semibold">Min. Ücret</th>
                <th className="text-left p-3 text-sm font-semibold">Max. Ücret</th>
                <th className="text-left p-3 text-sm font-semibold">Örnek</th>
              </tr>
            </thead>
            <tbody>
              {commissionTiers.map(t => (
                <tr key={t.category} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-semibold">{t.category}</td>
                  <td className="p-3 text-sm text-blue-700 font-semibold">{t.rate}</td>
                  <td className="p-3 text-sm">{t.minFee} TL</td>
                  <td className="p-3 text-sm">{t.maxFee} TL</td>
                  <td className="p-3 text-sm text-gray-500 text-xs">{t.example}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'history' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-left p-3 text-sm font-semibold">Ürün</th>
                <th className="text-right p-3 text-sm font-semibold">Satış Tutarı</th>
                <th className="text-right p-3 text-sm font-semibold">Komisyon</th>
                <th className="text-left p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {commissionHistory.map(h => (
                <tr key={h.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">{h.date}</td>
                  <td className="p-3 text-sm">{h.product}</td>
                  <td className="p-3 text-sm text-right">{h.saleAmount.toLocaleString()} TL</td>
                  <td className="p-3 text-sm text-right font-semibold text-blue-700">{h.commission.toFixed(2)} TL</td>
                  <td className="p-3 text-sm">
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold ${statusLabels[h.status]}`}>
                      {h.status === 'pending' ? 'Bekliyor' : 'Ödendi'}
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
