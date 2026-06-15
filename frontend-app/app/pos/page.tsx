'use client';
import { useState } from 'react';

const products = [
  { id: 1, name: 'Basic T-Shirt', sku: 'TRS-001', price: 29.99, stock: 42, category: 'Giyim' },
  { id: 2, name: 'Slim Fit Pantolon', sku: 'TRS-005', price: 89.99, stock: 28, category: 'Giyim' },
  { id: 3, name: 'Spor Ayakkabı', sku: 'SPR-001', price: 149.99, stock: 55, category: 'Ayakkabı' },
  { id: 4, name: 'Kazak - Klasik', sku: 'TRS-007', price: 69.99, stock: 18, category: 'Giyim' },
  { id: 5, name: 'Bileklik - Gümüş', sku: 'ACC-002', price: 39.99, stock: 33, category: 'Aksesuar' },
  { id: 6, name: 'Sırt Çantası', sku: 'BAG-001', price: 129.99, stock: 15, category: 'Aksesuar' },
  { id: 7, name: 'Şapka - Klasik', sku: 'HAT-001', price: 19.99, stock: 61, category: 'Aksesuar' },
  { id: 8, name: 'Denim Ceket', sku: 'TRS-010', price: 199.99, stock: 9, category: 'Giyim' },
];

type CartItem = { id: number; name: string; sku: string; price: number; quantity: number };

export default function POSPage() {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [search, setSearch] = useState('');
  const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card' | 'mobile'>('cash');
  const [paid, setPaid] = useState(false);

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) || p.sku.toLowerCase().includes(search.toLowerCase())
  );

  const addToCart = (product: typeof products[0]) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { id: product.id, name: product.name, sku: product.sku, price: product.price, quantity: 1 }];
    });
  };

  const updateQty = (id: number, delta: number) => {
    setCart(prev =>
      prev.map(item =>
        item.id === id ? { ...item, quantity: Math.max(1, item.quantity + delta) } : item
      ).filter(item => item.quantity > 0)
    );
  };

  const removeFromCart = (id: number) => {
    setCart(prev => prev.filter(item => item.id !== id));
  };

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const handlePayment = () => {
    setPaid(true);
    setTimeout(() => {
      setCart([]);
      setPaid(false);
    }, 3000);
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">POS Terminal</h1>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <input
            type="text"
            placeholder="Ürün ara (isim veya SKU)..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full border rounded-lg px-4 py-2 mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
          <div className="grid gap-3 grid-cols-2 sm:grid-cols-3">
            {filtered.map(p => (
              <button key={p.id} onClick={() => addToCart(p)}
                className="border rounded-lg p-3 text-left hover:border-blue-400 hover:shadow-sm transition-all text-sm">
                <p className="font-semibold truncate">{p.name}</p>
                <p className="text-xs text-gray-400 font-mono">{p.sku}</p>
                <p className="text-blue-700 font-bold mt-1">{p.price.toFixed(2)} TL</p>
                <p className="text-xs text-gray-400">Stok: {p.stock}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="border rounded-lg p-4 flex flex-col h-fit sticky top-20">
          <h2 className="font-bold text-lg mb-3">Sepet ({itemCount})</h2>
          {cart.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-8">Sepet boş</p>
          ) : (
            <>
              <div className="space-y-2 max-h-80 overflow-y-auto mb-4">
                {cart.map(item => (
                  <div key={item.id} className="flex items-center justify-between border-b pb-2 text-sm">
                    <div className="flex-1 min-w-0">
                      <p className="font-semibold truncate">{item.name}</p>
                      <p className="text-xs text-gray-400">{(item.price * item.quantity).toFixed(2)} TL</p>
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <button onClick={() => updateQty(item.id, -1)} className="w-6 h-6 rounded bg-gray-100 hover:bg-gray-200 text-xs font-bold">-</button>
                      <span className="w-6 text-center text-xs font-semibold">{item.quantity}</span>
                      <button onClick={() => updateQty(item.id, 1)} className="w-6 h-6 rounded bg-gray-100 hover:bg-gray-200 text-xs font-bold">+</button>
                      <button onClick={() => removeFromCart(item.id)} className="ml-1 text-red-500 hover:text-red-700 text-xs">×</button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t pt-3 mb-4">
                <div className="flex justify-between font-bold text-lg">
                  <span>Toplam</span>
                  <span className="text-blue-700">{total.toFixed(2)} TL</span>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 mb-2">Ödeme Yöntemi</p>
                <div className="flex gap-2">
                  {(['cash', 'card', 'mobile'] as const).map(m => (
                    <button key={m} onClick={() => setPaymentMethod(m)}
                      className={`flex-1 py-1.5 rounded text-xs font-semibold ${paymentMethod === m ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
                      {m === 'cash' ? 'Nakit' : m === 'card' ? 'Kart' : 'Mobil'}
                    </button>
                  ))}
                </div>
              </div>

              {paid ? (
                <div className="bg-green-100 text-green-800 text-center py-3 rounded-lg font-bold text-sm">
                  Ödeme Başarılı! ✓
                </div>
              ) : (
                <button onClick={handlePayment}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg font-semibold text-sm transition-colors">
                  Ödemeyi Tamamla ({total.toFixed(2)} TL)
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
