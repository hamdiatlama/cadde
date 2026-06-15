'use client';
import { useState } from 'react';

const balances = [
  { currency: 'TRY', label: 'Türk Lirası', balance: 45280.50, icon: '₺', color: 'text-red-600' },
  { currency: 'USD', label: 'Amerikan Doları', balance: 3240.00, icon: '$', color: 'text-green-600' },
  { currency: 'EUR', label: 'Euro', balance: 1850.75, icon: '€', color: 'text-blue-600' },
  { currency: 'GBP', label: 'İngiliz Sterlini', balance: 920.00, icon: '£', color: 'text-purple-600' },
];

const payoutHistory = [
  { id: 1, date: '2026-06-14', amount: 12500.00, currency: 'TRY', method: 'Banka Havalesi', status: 'completed', ref: 'P-2026-0614-001' },
  { id: 2, date: '2026-06-10', amount: 3400.00, currency: 'USD', method: 'Payoneer', status: 'completed', ref: 'P-2026-0610-002' },
  { id: 3, date: '2026-06-07', amount: 2100.00, currency: 'EUR', method: 'Banka Havalesi', status: 'pending', ref: 'P-2026-0607-003' },
  { id: 4, date: '2026-06-01', amount: 8900.00, currency: 'TRY', method: 'Banka Havalesi', status: 'completed', ref: 'P-2026-0601-004' },
  { id: 5, date: '2026-05-28', amount: 1500.00, currency: 'GBP', method: 'Payoneer', status: 'failed', ref: 'P-2026-0528-005' },
  { id: 6, date: '2026-05-25', amount: 6200.00, currency: 'TRY', method: 'Banka Havalesi', status: 'completed', ref: 'P-2026-0525-006' },
  { id: 7, date: '2026-05-20', amount: 2800.00, currency: 'USD', method: 'Payoneer', status: 'completed', ref: 'P-2026-0520-007' },
];

const schedulePref = {
  frequency: 'weekly',
  day: 'Pazartesi',
  minAmount: 100,
  method: 'bank',
};

export default function PayoutSchedulePage() {
  const [tab, setTab] = useState<'balances' | 'history' | 'settings'>('balances');

  const totalTRY = balances.reduce((sum, b) => {
    const rate = b.currency === 'TRY' ? 1 : b.currency === 'USD' ? 35.50 : b.currency === 'EUR' ? 38.20 : 45.10;
    return sum + b.balance * rate;
  }, 0);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Ödeme Takvimi</h1>
      <p className="text-gray-500 mb-6">Bakiyelerinizi görüntüleyin ve ödeme planınızı yönetin</p>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('balances')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'balances' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Bakiyeler</button>
        <button onClick={() => setTab('history')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'history' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Ödeme Geçmişi</button>
        <button onClick={() => setTab('settings')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'settings' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Plan</button>
      </div>

      {tab === 'balances' && (
        <>
          <div className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white rounded-xl p-6 mb-6 shadow-lg">
            <p className="text-sm opacity-80">Toplam Bakiye (TRY)</p>
            <p className="text-4xl font-bold mt-1">{totalTRY.toLocaleString('tr-TR', { minimumFractionDigits: 2 })} ₺</p>
            <p className="text-xs opacity-60 mt-1">Tüm para birimleri güncel kurdan hesaplanmıştır</p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {balances.map(b => (
              <div key={b.currency} className="border rounded-lg p-5">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-gray-500">{b.label}</span>
                  <span className={`text-xl font-bold ${b.color}`}>{b.icon}{b.currency}</span>
                </div>
                <p className="text-2xl font-bold">{b.balance.toLocaleString('tr-TR', { minimumFractionDigits: 2 })} {b.icon}</p>
                <button className="mt-3 text-xs text-blue-600 hover:text-blue-800 font-semibold">Ödeme Al</button>
              </div>
            ))}
          </div>
        </>
      )}

      {tab === 'history' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-left p-3 text-sm font-semibold">Referans</th>
                <th className="text-right p-3 text-sm font-semibold">Tutar</th>
                <th className="text-left p-3 text-sm font-semibold">Yöntem</th>
                <th className="text-center p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {payoutHistory.map(h => (
                <tr key={h.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">{h.date}</td>
                  <td className="p-3 text-sm font-mono text-gray-500">{h.ref}</td>
                  <td className="p-3 text-sm text-right font-semibold">{h.amount.toLocaleString('tr-TR', { minimumFractionDigits: 2 })} {h.currency}</td>
                  <td className="p-3 text-sm">{h.method}</td>
                  <td className="p-3 text-center">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                      h.status === 'completed' ? 'bg-green-100 text-green-700' :
                      h.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {h.status === 'completed' ? 'Tamamlandı' : h.status === 'pending' ? 'Bekliyor' : 'Başarısız'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'settings' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Ödeme Planı Ayarları</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">Ödeme Sıklığı</label>
              <select className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="daily">Günlük</option>
                <option value="weekly" selected>Haftalık</option>
                <option value="biweekly">İki Haftada Bir</option>
                <option value="monthly">Aylık</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">Ödeme Günü</label>
              <select className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>Pazartesi</option>
                <option>Salı</option>
                <option>Çarşamba</option>
                <option>Perşembe</option>
                <option selected>Cuma</option>
                <option>Cumartesi</option>
                <option>Pazar</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">Minimum Ödeme Tutarı</label>
              <input type="number" defaultValue={100} className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">Ödeme Yöntemi</label>
              <select className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="bank" selected>Banka Havalesi</option>
                <option value="payoneer">Payoneer</option>
                <option value="wise">Wise</option>
              </select>
            </div>
          </div>
          <button className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg text-sm font-semibold transition-colors">Kaydet</button>
        </div>
      )}
    </div>
  );
}
