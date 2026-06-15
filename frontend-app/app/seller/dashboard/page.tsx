'use client';
import { useState, useEffect } from 'react';

export default function SellerDashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [monthly, setMonthly] = useState<any[]>([]);
  const [top, setTop] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard/seller')
      .then(r => r.json())
      .then(d => { setStats(d.stats); setMonthly(d.monthly_sales); setTop(d.top_products); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Yukleniyor...</div>;
  if (!stats) return <div className="p-8 text-center">Satici hesabiniz bulunamadi</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Satici Panelim</h1>

      <div className="grid gap-4 md:grid-cols-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-blue-600">{stats.today_orders}</p><p className="text-sm text-gray-600">Bugun Siparis</p></div>
        <div className="bg-green-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-green-600">{stats.today_revenue} TL</p><p className="text-sm text-gray-600">Bugun Gelir</p></div>
        <div className="bg-yellow-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-yellow-600">{stats.pending_orders}</p><p className="text-sm text-gray-600">Bekleyen Siparis</p></div>
        <div className="bg-purple-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-purple-600">{stats.avg_rating}/5</p><p className="text-sm text-gray-600">Ortalama Puan</p></div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 mb-8">
        <div className="border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-3">Aylik Satislar</h2>
          {monthly.length === 0 && <p className="text-gray-500">Henuz veri yok</p>}
          {monthly.map((m: any) => (
            <div key={m.month} className="flex justify-between py-2 border-b">
              <span>{m.month}</span>
              <span className="font-semibold">{m.revenue} TL ({m.orders} siparis)</span>
            </div>
          ))}
        </div>
        <div className="border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-3">En Cok Satan Urunler</h2>
          {top.length === 0 && <p className="text-gray-500">Henuz veri yok</p>}
          {top.map((p: any) => (
            <div key={p.id} className="flex items-center gap-3 py-2 border-b">
              <img src={p.image_url || '/placeholder.png'} className="w-10 h-10 rounded" alt={p.name} />
              <div className="flex-1"><p className="font-medium">{p.name}</p><p className="text-sm text-gray-500">{p.sold_count} satis</p></div>
              <span className="font-semibold">{p.revenue} TL</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
