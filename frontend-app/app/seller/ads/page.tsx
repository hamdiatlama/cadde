'use client';
import { useState, useEffect } from 'react';

export default function AdsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/ads/campaigns').then(r => r.json()).then(setCampaigns);
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Reklam Yonetimi</h1>
      <a href="/seller/ads/new" className="bg-blue-600 text-white px-4 py-2 rounded inline-block mb-4 hover:bg-blue-700">Yeni Kampanya</a>
      <div className="grid gap-4">
        {campaigns.map((c: any) => (
          <div key={c.id} className="border rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-start">
              <div><h3 className="font-semibold text-lg">{c.name}</h3><p className="text-sm text-gray-500">{c.type}</p></div>
              <span className={'px-2 py-1 rounded text-sm ' + (c.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600')}>{c.is_active ? 'Aktif' : 'Pasif'}</span>
            </div>
            <div className="grid grid-cols-4 gap-4 mt-4 text-center text-sm">
              <div><p className="font-bold">{c.impressions}</p><p className="text-gray-500">Gosterim</p></div>
              <div><p className="font-bold">{c.clicks}</p><p className="text-gray-500">Tiklama</p></div>
              <div><p className="font-bold">{c.spent} TL</p><p className="text-gray-500">Harcanan</p></div>
              <div><p className="font-bold">{c.total_budget} TL</p><p className="text-gray-500">Butce</p></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
