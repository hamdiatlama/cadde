'use client';
import { useState, useEffect } from 'react';

export default function ComparePage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/compare/')
      .then(r => r.json())
      .then(d => setProducts(d.products || []))
      .finally(() => setLoading(false));
  }, []);

  async function removeProduct(productId: number) {
    await fetch('/api/compare/' + productId, { method: 'DELETE' });
    setProducts(products.filter(p => p.id !== productId));
  }

  if (loading) return <div className="p-8 text-center">Yukleniyor...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Urun Karsilastirma</h1>
      {products.length === 0 && <p className="text-gray-500">Henuz karsilastirilacak urun yok. Urun sayfasindan karsilastirmaya ekleyin.</p>}
      {products.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100">
                <th className="p-3 text-left">Ozellik</th>
                {products.map(p => (
                  <th key={p.id} className="p-3 text-center">
                    <img src={p.image_url || '/placeholder.png'} className="h-24 mx-auto mb-2" alt={p.name} />
                    <p className="font-semibold">{p.name}</p>
                    <button onClick={() => removeProduct(p.id)} className="text-red-500 text-xs">Kaldir</button>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr className="border-b"><td className="p-3 font-medium">Fiyat</td>
                {products.map(p => <td key={p.id} className="p-3 text-center"><span className={p.compare_price ? 'line-through text-gray-400' : ''}>{p.price} TL</span>{p.compare_price && <span className="text-red-600 ml-2">{p.compare_price} TL</span>}</td>)}
              </tr>
              <tr className="border-b"><td className="p-3 font-medium">Kategori</td>
                {products.map(p => <td key={p.id} className="p-3 text-center">{p.category || '-'}</td>)}
              </tr>
              <tr className="border-b"><td className="p-3 font-medium">Puan</td>
                {products.map(p => <td key={p.id} className="p-3 text-center">{'★'.repeat(Math.round(p.rating))} ({p.review_count})</td>)}
              </tr>
              <tr className="border-b"><td className="p-3 font-medium">Stok</td>
                {products.map(p => <td key={p.id} className="p-3 text-center">{p.stock > 0 ? 'Stokta' : 'Tukendi'}</td>)}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
