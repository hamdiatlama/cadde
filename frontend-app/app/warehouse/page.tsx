'use client';
import { useState } from 'react';

const warehouses = [
  { id: 1, name: 'Merkez Depo', location: 'İstanbul', capacity: '80%', itemCount: 12450, status: 'Aktif' },
  { id: 2, name: 'Ankara Şube', location: 'Ankara', capacity: '45%', itemCount: 5620, status: 'Aktif' },
  { id: 3, name: 'İzmir Lojistik', location: 'İzmir', capacity: '92%', itemCount: 8900, status: 'Aktif' },
  { id: 4, name: 'Bursa Depo', location: 'Bursa', capacity: '30%', itemCount: 2100, status: 'Pasif' },
];

const stockItems = [
  { name: 'Basic T-Shirt (Kırmızı/M)', sku: 'TRS-001', warehouse: 'Merkez Depo', stock: 42, minLevel: 20 },
  { name: 'Basic T-Shirt (Mavi/L)', sku: 'TRS-002', warehouse: 'Merkez Depo', stock: 28, minLevel: 20 },
  { name: 'Slim Fit Pantolon (Siyah/L)', sku: 'TRS-005', warehouse: 'Ankara Şube', stock: 8, minLevel: 15 },
  { name: 'Slim Fit Pantolon (Mavi/M)', sku: 'TRS-006', warehouse: 'İzmir Lojistik', stock: 3, minLevel: 15 },
  { name: 'Kazak (Yeşil/XL)', sku: 'TRS-007', warehouse: 'Merkez Depo', stock: 0, minLevel: 10 },
  { name: 'Spor Ayakkabı (42)', sku: 'SPR-001', warehouse: 'İzmir Lojistik', stock: 55, minLevel: 30 },
  { name: 'Spor Ayakkabı (43)', sku: 'SPR-002', warehouse: 'Ankara Şube', stock: 12, minLevel: 30 },
];

export default function WarehousePage() {
  const [activeTab, setActiveTab] = useState<'depolar' | 'stok'>('depolar');

  const lowStock = stockItems.filter(s => s.stock < s.minLevel);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Depo Yönetimi</h1>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setActiveTab('depolar')} className={`px-4 py-2 rounded-lg text-sm font-semibold ${activeTab === 'depolar' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Depolar</button>
        <button onClick={() => setActiveTab('stok')} className={`px-4 py-2 rounded-lg text-sm font-semibold ${activeTab === 'stok' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Stok Seviyeleri</button>
      </div>

      {activeTab === 'depolar' && (
        <div className="grid gap-4 md:grid-cols-2">
          {warehouses.map(w => (
            <div key={w.id} className="border rounded-lg p-5">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-lg">{w.name}</h3>
                  <p className="text-sm text-gray-500">{w.location}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-semibold ${w.status === 'Aktif' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>{w.status}</span>
              </div>
              <div className="mb-3">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-500">Kapasite</span>
                  <span className="font-semibold">{w.capacity}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 rounded-full h-2" style={{ width: w.capacity }}></div>
                </div>
              </div>
              <p className="text-sm text-gray-500">{w.itemCount.toLocaleString()} ürün</p>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'stok' && (
        <>
          {lowStock.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-red-800 mb-2">Düşük Stok Uyarıları ({lowStock.length})</h3>
              <div className="space-y-2">
                {lowStock.map(s => (
                  <div key={s.sku} className="flex justify-between items-center text-sm">
                    <span className="text-red-700">{s.name} ({s.sku})</span>
                    <span className="text-red-600 font-semibold">{s.stock} / {s.minLevel} (min.)</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="text-left p-3 text-sm font-semibold">Ürün</th>
                  <th className="text-left p-3 text-sm font-semibold">SKU</th>
                  <th className="text-left p-3 text-sm font-semibold">Depo</th>
                  <th className="text-right p-3 text-sm font-semibold">Stok</th>
                  <th className="text-right p-3 text-sm font-semibold">Min. Seviye</th>
                  <th className="text-left p-3 text-sm font-semibold">Durum</th>
                </tr>
              </thead>
              <tbody>
                {stockItems.map(s => {
                  const isLow = s.stock < s.minLevel;
                  const isOut = s.stock === 0;
                  return (
                    <tr key={s.sku} className="border-b hover:bg-gray-50">
                      <td className="p-3 text-sm">{s.name}</td>
                      <td className="p-3 text-sm font-mono">{s.sku}</td>
                      <td className="p-3 text-sm">{s.warehouse}</td>
                      <td className={`p-3 text-sm text-right font-semibold ${isOut ? 'text-red-600' : isLow ? 'text-yellow-600' : ''}`}>{s.stock}</td>
                      <td className="p-3 text-sm text-right">{s.minLevel}</td>
                      <td className="p-3 text-sm">
                        <span className={`px-2 py-0.5 rounded text-xs font-semibold ${isOut ? 'bg-red-100 text-red-800' : isLow ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}>
                          {isOut ? 'Tükendi' : isLow ? 'Düşük' : 'Normal'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
