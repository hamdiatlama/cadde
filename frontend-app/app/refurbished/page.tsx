'use client';
import { useState } from 'react';

const products = [
  { id: 1, title: 'iPhone 14 Pro 128GB', condition: 'Mükemmel', originalPrice: 24999, price: 17999, warranty: '12 Ay', category: 'Telefon' },
  { id: 2, title: 'MacBook Air M1', condition: 'Çok İyi', originalPrice: 34999, price: 21999, warranty: '6 Ay', category: 'Bilgisayar' },
  { id: 3, title: 'Sony WH-1000XM5', condition: 'Mükemmel', originalPrice: 5999, price: 3999, warranty: '12 Ay', category: 'Kulaklık' },
  { id: 4, title: 'Samsung Galaxy Tab S8', condition: 'İyi', originalPrice: 12999, price: 8499, warranty: '6 Ay', category: 'Tablet' },
  { id: 5, title: 'Canon EOS R6', condition: 'Çok İyi', originalPrice: 45999, price: 32999, warranty: '12 Ay', category: 'Kamera' },
  { id: 6, title: 'Dyson V15 Detect', condition: 'Mükemmel', originalPrice: 12999, price: 8999, warranty: '6 Ay', category: 'Ev Aleti' },
  { id: 7, title: 'PlayStation 5 Dijital', condition: 'İyi', originalPrice: 15999, price: 11999, warranty: '3 Ay', category: 'Konsol' },
  { id: 8, title: 'Apple Watch Series 8', condition: 'Mükemmel', originalPrice: 9999, price: 6999, warranty: '12 Ay', category: 'Giyilebilir' },
];

const conditions = ['Tümü', 'Mükemmel', 'Çok İyi', 'İyi'];
const categories = [...new Set(products.map(p => p.category))];

const conditionColors: Record<string, string> = {
  'Mükemmel': 'bg-green-100 text-green-800',
  'Çok İyi': 'bg-blue-100 text-blue-800',
  'İyi': 'bg-yellow-100 text-yellow-800',
};

export default function RefurbishedPage() {
  const [conditionFilter, setConditionFilter] = useState('Tümü');
  const [categoryFilter, setCategoryFilter] = useState('Tümü');

  const filtered = products.filter(p => {
    if (conditionFilter !== 'Tümü' && p.condition !== conditionFilter) return false;
    if (categoryFilter !== 'Tümü' && p.category !== categoryFilter) return false;
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Yenilenmiş Ürünler</h1>
      <p className="text-gray-500 mb-6">Test edilmiş, onarılmış, garantili ikinci el ürünler</p>

      <div className="flex flex-wrap gap-2 mb-4">
        {conditions.map(c => (
          <button key={c} onClick={() => setConditionFilter(c)}
            className={`px-3 py-1.5 rounded text-sm font-semibold ${conditionFilter === c ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {c}
          </button>
        ))}
      </div>
      <div className="flex gap-2 mb-6">
        {['Tümü', ...categories].map(c => (
          <button key={c} onClick={() => setCategoryFilter(c)}
            className={`px-3 py-1.5 rounded text-sm ${categoryFilter === c ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {c}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filtered.map(p => {
          const discount = Math.round((1 - p.price / p.originalPrice) * 100);
          return (
            <div key={p.id} className="border rounded-lg shadow-sm hover:shadow-md overflow-hidden">
              <div className="h-36 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center text-gray-400 text-sm">
                Ürün Görseli
              </div>
              <div className="p-4">
                <span className={`inline-block text-xs px-2 py-0.5 rounded font-semibold mb-2 ${conditionColors[p.condition]}`}>
                  {p.condition}
                </span>
                <h2 className="font-semibold text-sm mb-2 line-clamp-2">{p.title}</h2>
                <div className="mb-2">
                  <p className="text-xl font-bold text-blue-700">{p.price.toLocaleString()} TL</p>
                  <p className="text-xs text-gray-400 line-through">{p.originalPrice.toLocaleString()} TL</p>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
                  <span>{p.warranty} garanti</span>
                  <span className="text-green-600 font-semibold">%{discount} indirim</span>
                </div>
                <button className="w-full bg-blue-600 text-white py-2 rounded-lg text-sm hover:bg-blue-700">
                  Sepete Ekle
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
