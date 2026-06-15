'use client';
import { useState } from 'react';

const defaultGroups = [
  { id: 1, name: 'Renk', options: ['Kırmızı', 'Mavi', 'Siyah', 'Beyaz', 'Yeşil'] },
  { id: 2, name: 'Beden', options: ['S', 'M', 'L', 'XL', 'XXL'] },
  { id: 3, name: 'Malzeme', options: ['Pamuk', 'Polyester', 'Yün'] },
];

const defaultSkus = [
  { sku: 'TRS-001', product: 'Basic T-Shirt', variant: 'Kırmızı / M', price: 149, stock: 42, barcode: '8691234567890' },
  { sku: 'TRS-002', product: 'Basic T-Shirt', variant: 'Mavi / L', price: 149, stock: 28, barcode: '8691234567891' },
  { sku: 'TRS-003', product: 'Basic T-Shirt', variant: 'Siyah / S', price: 159, stock: 0, barcode: '8691234567892' },
  { sku: 'TRS-004', product: 'Basic T-Shirt', variant: 'Beyaz / XL', price: 169, stock: 15, barcode: '8691234567893' },
  { sku: 'TRS-005', product: 'Slim Fit Pantolon', variant: 'Siyah / L', price: 299, stock: 8, barcode: '8691234567894' },
  { sku: 'TRS-006', product: 'Slim Fit Pantolon', variant: 'Mavi / M', price: 279, stock: 3, barcode: '8691234567895' },
  { sku: 'TRS-007', product: 'Kazak', variant: 'Yeşil / XL', price: 199, stock: 0, barcode: '8691234567896' },
];

export default function VariantsPage() {
  const [groups] = useState(defaultGroups);
  const [skus] = useState(defaultSkus);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Varyant / SKU Yönetimi</h1>

      <div className="grid gap-6 md:grid-cols-3 mb-8">
        {groups.map(g => (
          <div key={g.id} className="border rounded-lg p-4">
            <h2 className="font-semibold text-lg mb-3">{g.name}</h2>
            <div className="flex flex-wrap gap-2">
              {g.options.map(o => (
                <span key={o} className="bg-gray-100 px-3 py-1 rounded text-sm">{o}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <h2 className="text-xl font-semibold mb-4">SKU Tablosu</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="text-left p-3 text-sm font-semibold">SKU</th>
              <th className="text-left p-3 text-sm font-semibold">Ürün</th>
              <th className="text-left p-3 text-sm font-semibold">Varyant</th>
              <th className="text-right p-3 text-sm font-semibold">Fiyat</th>
              <th className="text-right p-3 text-sm font-semibold">Stok</th>
              <th className="text-left p-3 text-sm font-semibold">Barkod</th>
            </tr>
          </thead>
          <tbody>
            {skus.map(s => (
              <tr key={s.sku} className="border-b hover:bg-gray-50">
                <td className="p-3 text-sm font-mono">{s.sku}</td>
                <td className="p-3 text-sm">{s.product}</td>
                <td className="p-3 text-sm">{s.variant}</td>
                <td className="p-3 text-sm text-right">{s.price} TL</td>
                <td className="p-3 text-sm text-right">
                  <span className={s.stock === 0 ? 'text-red-600 font-semibold' : ''}>{s.stock}</span>
                </td>
                <td className="p-3 text-sm font-mono">{s.barcode}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
