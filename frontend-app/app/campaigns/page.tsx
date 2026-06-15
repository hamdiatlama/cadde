'use client';
import { useState, useEffect } from 'react';

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [flashSales, setFlashSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/api/campaigns/').then(r => r.json()),
      fetch('/api/campaigns/flash-sales').then(r => r.json()),
    ]).then(([c, f]) => { setCampaigns(c); setFlashSales(f); }).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Yukleniyor...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Kampanyalar</h1>

      {flashSales.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Firsat Urunleri</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {flashSales.map((fs: any) => (
              <div key={fs.id} className="border rounded-lg p-4 shadow-sm relative">
                <span className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-xs">FIRSAT</span>
                <img src={fs.product_image || '/placeholder.png'} className="h-32 mx-auto mb-3" alt={fs.product_name} />
                <h3 className="font-semibold">{fs.product_name}</h3>
                <div className="flex gap-2 items-center mt-2">
                  <span className="text-2xl font-bold text-red-600">{fs.sale_price} TL</span>
                  <span className="line-through text-gray-400">{fs.original_price} TL</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div className="bg-red-500 rounded-full h-2" style={{width: Math.min(100, (fs.sold_count/fs.quantity_limit)*100)+'%'}}></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">{fs.sold_count}/{fs.quantity_limit} satildi</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <h2 className="text-xl font-semibold mb-4">Aktif Kampanyalar</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {campaigns.map((c: any) => (
          <div key={c.id} className="border rounded-lg p-4 shadow-sm" style={c.banner_url ? {backgroundImage: `url(${c.banner_url})`, backgroundSize: 'cover'} : {}}>
            <h3 className="font-bold text-lg">{c.name}</h3>
            <p className="text-sm text-gray-600">{c.description}</p>
            <div className="mt-2">
              {c.discount_type === 'percentage' && <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">%{c.discount_value} indirim</span>}
              {c.discount_type === 'fixed' && <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">{c.discount_value} TL indirim</span>}
              {c.discount_type === 'free_shipping' && <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Ucretsiz kargo</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
