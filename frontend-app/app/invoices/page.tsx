'use client';
import { useState } from 'react';

const invoices = [
  { id: 'INV-2026-001', date: '2026-06-14', customer: 'Mehmet Usta', amount: 2980, status: 'paid', type: 'Satış' },
  { id: 'INV-2026-002', date: '2026-06-13', customer: 'Ayşe Tekstil', amount: 7450, status: 'paid', type: 'Satış' },
  { id: 'INV-2026-003', date: '2026-06-12', customer: 'Ali Bey', amount: 520, status: 'pending', type: 'Satış' },
  { id: 'INV-2026-004', date: '2026-06-11', customer: 'Can Market', amount: 15000, status: 'paid', type: 'Satış' },
  { id: 'INV-2026-005', date: '2026-06-10', customer: 'Zeynep Hanım', amount: 890, status: 'cancelled', type: 'Satış' },
  { id: 'INV-2026-006', date: '2026-06-09', customer: 'Depo Kira', amount: 5000, status: 'paid', type: 'Gider' },
  { id: 'INV-2026-007', date: '2026-06-08', customer: 'Reklam Hizmeti', amount: 2000, status: 'pending', type: 'Gider' },
];

const statusLabels: Record<string, { label: string; style: string }> = {
  paid: { label: 'Ödendi', style: 'bg-green-100 text-green-800' },
  pending: { label: 'Bekliyor', style: 'bg-yellow-100 text-yellow-800' },
  cancelled: { label: 'İptal', style: 'bg-red-100 text-red-800' },
};

export default function InvoicesPage() {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState<'date' | 'amount'>('date');

  const filtered = invoices
    .filter(i => filter === 'all' || i.type === filter)
    .sort((a, b) => sortBy === 'amount' ? b.amount - a.amount : new Date(b.date).getTime() - new Date(a.date).getTime());

  const totalAmount = filtered.reduce((a, i) => a + i.amount, 0);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Faturalar ve Vergiler</h1>
      <p className="text-gray-500 mb-6">E-fatura kayıtlarınızı görüntüleyin ve yönetin</p>

      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-blue-700">{invoices.filter(i => i.status === 'paid').length}</p>
          <p className="text-sm text-gray-600">Ödenmiş Fatura</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-yellow-700">{invoices.filter(i => i.status === 'pending').length}</p>
          <p className="text-sm text-gray-600">Bekleyen Fatura</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg text-center">
          <p className="text-2xl font-bold text-green-700">{totalAmount.toLocaleString()} TL</p>
          <p className="text-sm text-gray-600">Toplam Tutar</p>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-4">
        <div className="flex gap-1">
          {['all', 'Satış', 'Gider'].map(f => (
            <button key={f} onClick={() => setFilter(f)} className={`px-3 py-1.5 rounded text-sm font-semibold ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
              {f === 'all' ? 'Tümü' : f}
            </button>
          ))}
        </div>
        <div className="ml-auto">
          <select value={sortBy} onChange={e => setSortBy(e.target.value as any)} className="border rounded-lg p-1.5 text-sm">
            <option value="date">Tarihe Göre</option>
            <option value="amount">Tutara Göre</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="text-left p-3 text-sm font-semibold">Fatura No</th>
              <th className="text-left p-3 text-sm font-semibold">Tarih</th>
              <th className="text-left p-3 text-sm font-semibold">Alıcı / Tedarikçi</th>
              <th className="text-left p-3 text-sm font-semibold">Tür</th>
              <th className="text-right p-3 text-sm font-semibold">Tutar</th>
              <th className="text-left p-3 text-sm font-semibold">Durum</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(inv => (
              <tr key={inv.id} className="border-b hover:bg-gray-50">
                <td className="p-3 text-sm font-mono">{inv.id}</td>
                <td className="p-3 text-sm">{inv.date}</td>
                <td className="p-3 text-sm">{inv.customer}</td>
                <td className="p-3 text-sm">{inv.type}</td>
                <td className="p-3 text-sm text-right font-semibold">{inv.amount.toLocaleString()} TL</td>
                <td className="p-3 text-sm">
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${statusLabels[inv.status].style}`}>
                    {statusLabels[inv.status].label}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 text-right">
        <button className="bg-blue-600 text-white px-5 py-2 rounded-lg text-sm hover:bg-blue-700">
          PDF Olarak İndir
        </button>
      </div>
    </div>
  );
}
