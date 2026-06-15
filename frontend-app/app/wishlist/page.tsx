'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function WishlistPage() {
  const [wishlists, setWishlists] = useState<any[]>([]);
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => { fetchWishlists(); }, []);

  async function fetchWishlists() {
    try {
      const res = await fetch('/api/wishlist/');
      if (res.ok) setWishlists(await res.json());
    } catch { setError('Giris yapmalisiniz'); }
    finally { setLoading(false); }
  }

  async function createWishlist() {
    if (!name.trim()) return;
    const res = await fetch('/api/wishlist/?name=' + encodeURIComponent(name) + '&is_public=false', { method: 'POST' });
    if (res.ok) { setWishlists(await res.json()); setName(''); await fetchWishlists(); }
  }

  async function deleteWishlist(id: number) {
    await fetch('/api/wishlist/' + id, { method: 'DELETE' });
    await fetchWishlists();
  }

  if (loading) return <div className="p-8 text-center">Yukleniyor...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Favori Listelerim</h1>
      {error && <div className="bg-yellow-100 p-4 rounded mb-4">{error}</div>}
      <div className="flex gap-2 mb-6">
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Yeni liste adi"
          className="border p-2 flex-1 rounded" onKeyDown={e => e.key === 'Enter' && createWishlist()} />
        <button onClick={createWishlist} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Olustur</button>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {wishlists.map((wl: any) => (
          <div key={wl.id} className="border rounded-lg p-4 shadow-sm hover:shadow-md">
            <div className="flex justify-between items-start">
              <div>
                <Link href={'/wishlist/' + wl.id} className="text-lg font-semibold text-blue-600 hover:underline">
                  {wl.name}
                </Link>
                <p className="text-sm text-gray-500">{wl.item_count} urun</p>
                {wl.share_code && <p className="text-xs text-gray-400">Kod: {wl.share_code}</p>}
              </div>
              <button onClick={() => deleteWishlist(wl.id)} className="text-red-500 text-sm hover:underline">Sil</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
