'use client';
import { useState } from 'react';

const transactions = [
  { id: 1, type: 'deposit', amount: 5000, description: 'Kredi Kartı ile Yatırma', date: '2026-06-14 10:30', status: 'completed' },
  { id: 2, type: 'withdraw', amount: -1200, description: 'Havale ile Çekim', date: '2026-06-13 14:15', status: 'completed' },
  { id: 3, type: 'deposit', amount: 2000, description: 'Havale ile Yatırma', date: '2026-06-12 09:00', status: 'pending' },
  { id: 4, type: 'payment', amount: -349, description: 'Sipariş #ORD-2026-0421', date: '2026-06-11 16:45', status: 'completed' },
  { id: 5, type: 'refund', amount: 149, description: 'İade #RET-2026-001', date: '2026-06-10 11:20', status: 'completed' },
  { id: 6, type: 'withdraw', amount: -3000, description: 'Banka Hesabına Çekim', date: '2026-06-09 08:00', status: 'completed' },
  { id: 7, type: 'deposit', amount: 10000, description: 'EFT ile Yatırma', date: '2026-06-08 13:00', status: 'completed' },
];

const statusStyles: Record<string, string> = {
  completed: 'bg-green-100 text-green-800',
  pending: 'bg-yellow-100 text-yellow-800',
  failed: 'bg-red-100 text-red-800',
};

export default function WalletPage() {
  const [tab, setTab] = useState<'deposit' | 'withdraw' | 'history'>('history');
  const [depositAmount, setDepositAmount] = useState(0);
  const [withdrawAmount, setWithdrawAmount] = useState(0);
  const balance = 8750;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Cüzdan</h1>
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-xl p-6 shadow-lg">
          <p className="text-sm opacity-80 mb-1">Mevcut Bakiye</p>
          <p className="text-4xl font-bold">{balance.toLocaleString()} TL</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6">
        {(['deposit', 'withdraw', 'history'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === t ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {t === 'deposit' ? 'Para Yatır' : t === 'withdraw' ? 'Para Çek' : 'İşlem Geçmişi'}
          </button>
        ))}
      </div>

      {tab === 'deposit' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Para Yatır</h2>
          <div className="flex gap-2 mb-4 flex-wrap">
            {[500, 1000, 2500, 5000, 10000].map(a => (
              <button key={a} onClick={() => setDepositAmount(a)}
                className={`px-4 py-2 rounded-lg border text-sm font-semibold ${depositAmount === a ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 text-gray-700 hover:border-blue-400'}`}>
                {a.toLocaleString()} TL
              </button>
            ))}
          </div>
          <div className="flex gap-2 mb-4">
            <input type="number" value={depositAmount || ''} onChange={e => setDepositAmount(Number(e.target.value))}
              placeholder="Tutar girin" className="border rounded-lg p-2 flex-1 text-sm" />
            <button onClick={() => alert(`${depositAmount} TL yatırma talebi alındı`)}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700">
              Yatır
            </button>
          </div>
        </div>
      )}

      {tab === 'withdraw' && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Para Çek</h2>
          <p className="text-sm text-gray-500 mb-3">Çekim talebi banka hesabınıza 1-3 iş günü içinde yapılır.</p>
          <div className="flex gap-2 mb-4">
            <input type="number" value={withdrawAmount || ''} onChange={e => setWithdrawAmount(Number(e.target.value))}
              placeholder="Tutar girin" max={balance} className="border rounded-lg p-2 flex-1 text-sm" />
            <button onClick={() => alert(`${withdrawAmount} TL çekim talebi alındı`)}
              className="bg-gray-800 text-white px-6 py-2 rounded-lg text-sm hover:bg-gray-900">
              Çek
            </button>
          </div>
          <p className="text-xs text-gray-400">Çekilebilir bakiye: {balance.toLocaleString()} TL</p>
        </div>
      )}

      {tab === 'history' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">İşlem</th>
                <th className="text-left p-3 text-sm font-semibold">Açıklama</th>
                <th className="text-left p-3 text-sm font-semibold">Tarih</th>
                <th className="text-right p-3 text-sm font-semibold">Tutar</th>
                <th className="text-left p-3 text-sm font-semibold">Durum</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(tx => (
                <tr key={tx.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">
                    <span className={`font-semibold ${tx.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {tx.amount > 0 ? 'Yatırma' : tx.type === 'refund' ? 'İade' : tx.type === 'payment' ? 'Ödeme' : 'Çekim'}
                    </span>
                  </td>
                  <td className="p-3 text-sm text-gray-600">{tx.description}</td>
                  <td className="p-3 text-sm">{tx.date}</td>
                  <td className={`p-3 text-sm text-right font-semibold ${tx.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {tx.amount > 0 ? '+' : ''}{tx.amount.toLocaleString()} TL
                  </td>
                  <td className="p-3 text-sm">
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold ${statusStyles[tx.status]}`}>
                      {tx.status === 'completed' ? 'Tamamlandı' : tx.status === 'pending' ? 'Bekliyor' : 'Başarısız'}
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
