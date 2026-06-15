'use client';
import { useState } from 'react';

const tiers = [
  { range: '1-50 adet', discount: '0%', price: 149 },
  { range: '51-200 adet', discount: '10%', price: 134 },
  { range: '201-500 adet', discount: '20%', price: 119 },
  { range: '501-1000 adet', discount: '30%', price: 104 },
  { range: '1000+ adet', discount: '40%', price: 89 },
];

const products = [
  { name: 'Basic T-Shirt', basePrice: 149, tiers: [149, 134, 119, 104, 89] },
  { name: 'Slim Fit Pantolon', basePrice: 299, tiers: [299, 269, 239, 209, 179] },
  { name: 'Kazak', basePrice: 199, tiers: [199, 179, 159, 139, 119] },
  { name: 'Spor Ayakkabı', basePrice: 399, tiers: [399, 359, 319, 279, 239] },
];

export default function B2bPage() {
  const [selectedProduct, setSelectedProduct] = useState(0);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">B2B Toptan Fiyatlandırma</h1>
      <p className="text-gray-500 mb-6">Kurumsal müşterilere özel hacim bazlı fiyat tabloları</p>

      <div className="grid gap-6 md:grid-cols-5 mb-8">
        {tiers.map((t, i) => (
          <div key={i} className={`border rounded-lg p-4 text-center ${i === 4 ? 'bg-blue-50 border-blue-300' : ''}`}>
            <p className="text-sm text-gray-500 mb-1">{t.range}</p>
            <p className="text-2xl font-bold text-blue-700">{t.price} TL</p>
            <p className="text-sm text-green-600 font-semibold">{t.discount} indirim</p>
          </div>
        ))}
      </div>

      <h2 className="text-xl font-semibold mb-4">Ürün Bazlı Fiyat Tablosu</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="text-left p-3 text-sm font-semibold">Ürün</th>
              <th className="text-left p-3 text-sm font-semibold">Baz Fiyat</th>
              <th className="text-left p-3 text-sm font-semibold">1-50</th>
              <th className="text-left p-3 text-sm font-semibold">51-200</th>
              <th className="text-left p-3 text-sm font-semibold">201-500</th>
              <th className="text-left p-3 text-sm font-semibold">501-1000</th>
              <th className="text-left p-3 text-sm font-semibold">1000+</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p, i) => (
              <tr
                key={p.name}
                onClick={() => setSelectedProduct(i)}
                className={`border-b hover:bg-gray-50 cursor-pointer ${selectedProduct === i ? 'bg-blue-50' : ''}`}
              >
                <td className="p-3 text-sm font-semibold">{p.name}</td>
                <td className="p-3 text-sm">{p.basePrice} TL</td>
                {p.tiers.map((t, j) => (
                  <td key={j} className="p-3 text-sm font-semibold text-blue-700">{t} TL</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 bg-gray-50 border rounded-lg p-6">
        <h3 className="font-semibold text-lg mb-3">Toplu Sipariş Talebi</h3>
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Ürün</label>
            <select className="w-full border rounded-lg p-2 text-sm">
              {products.map(p => <option key={p.name}>{p.name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Adet</label>
            <input type="number" placeholder="0" className="w-full border rounded-lg p-2 text-sm" />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">&nbsp;</label>
            <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
              Teklif İste
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
