'use client';
import { useState, useEffect } from 'react';

export default function PayoutsPage() {
  const [earnings, setEarnings] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/payouts/earnings').then(r => r.json()).then(setEarnings);
    fetch('/api/payouts/history').then(r => r.json()).then(setHistory);
  }, []);

  async function requestPayout() {
    const res = await fetch('/api/payouts/request', { method: 'POST' });
    if (res.ok) {
      alert('Odeme talebi alindi');
      window.location.reload();
    } else {
      const err = await res.json();
      alert(err.detail || 'Hata');
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Odeme ve Kazanc</h1>

      {earnings && (
        <div className="grid gap-4 md:grid-cols-3 mb-8">
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <p className="text-2xl font-bold text-green-600">{earnings.total_sales_30d} TL</p>
            <p className="text-sm text-gray-600">30 Gunluk Satis</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <p className="text-2xl font-bold text-blue-600">{earnings.pending_escrow} TL</p>
            <p className="text-sm text-gray-600">Bekleyen Bakiye</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <p className="text-2xl font-bold text-purple-600">{earnings.released_30d} TL</p>
            <p className="text-sm text-gray-600">Son 30 Gun Odenen</p>
          </div>
        </div>
      )}

      <button onClick={requestPayout} className="bg-green-600 text-white px-6 py-3 rounded-lg text-lg mb-8 hover:bg-green-700">
        Odeme Talebi Olustur
      </button>

      <h2 className="text-xl font-semibold mb-4">Odeme Gecmisi</h2>
      <div className="space-y-3">
        {history.map((p: any) => (
          <div key={p.id} className="border rounded-lg p-4 flex justify-between items-center">
            <div>
              <p className="font-semibold">{p.net_amount} TL</p>
              <p className="text-sm text-gray-500">{p.created_at}</p>
            </div>
            <span className={'px-3 py-1 rounded text-sm ' + (p.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800')}>
              {p.status === 'paid' ? 'Odendi' : 'Bekliyor'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
