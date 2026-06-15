'use client';
import { useState } from 'react';

const savedCards = [
  { id: 1, brand: 'visa', last4: '4242', holder: 'Ahmet Yılmaz', expMonth: 12, expYear: 2028, default: true },
  { id: 2, brand: 'mastercard', last4: '5678', holder: 'Ahmet Yılmaz', expMonth: 8, expYear: 2027, default: false },
  { id: 3, brand: 'amex', last4: '3456', holder: 'Ahmet Yılmaz', expMonth: 3, expYear: 2029, default: false },
];

const brandIcons: Record<string, string> = {
  visa: 'VISA',
  mastercard: 'MC',
  amex: 'AMEX',
  troy: 'TROY',
};

const brandColors: Record<string, string> = {
  visa: 'bg-blue-600',
  mastercard: 'bg-orange-500',
  amex: 'bg-blue-800',
  troy: 'bg-red-600',
};

type PaymentMethod = { id: number; type: 'card' | 'iban' | 'mobile'; label: string; details: string; default: boolean };

const otherMethods: PaymentMethod[] = [
  { id: 4, type: 'iban', label: 'Ziraat Bankası', details: 'TR12 0006 2000 1234 5678 9012 34', default: false },
  { id: 5, type: 'mobile', label: 'Turkcell Cüzdan', details: '05XX XXX XX 12', default: false },
];

export default function SavedCardsPage() {
  const [showAdd, setShowAdd] = useState(false);
  const [cards, setCards] = useState(savedCards);
  const [methods, setMethods] = useState(otherMethods);

  const setDefaultCard = (id: number) => {
    setCards(prev => prev.map(c => ({ ...c, default: c.id === id })));
  };

  const removeCard = (id: number) => {
    setCards(prev => prev.filter(c => c.id !== id));
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Kayıtlı Kartlar</h1>
      <p className="text-gray-500 mb-6">Ödeme yöntemlerinizi yönetin</p>

      <div className="space-y-4 mb-8">
        <h2 className="text-lg font-semibold">Kredi / Banka Kartları</h2>
        {cards.map(card => (
          <div key={card.id} className={`border rounded-lg p-4 flex items-center gap-4 ${card.default ? 'ring-2 ring-blue-500 bg-blue-50' : ''}`}>
            <div className={`w-14 h-9 rounded flex items-center justify-center text-[10px] font-bold text-white ${brandColors[card.brand]}`}>
              {brandIcons[card.brand]}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-sm">
                {card.brand.charAt(0).toUpperCase() + card.brand.slice(1)} •••• {card.last4}
              </p>
              <p className="text-xs text-gray-500">{card.holder} - Geçerlilik: {card.expMonth}/{card.expYear}</p>
            </div>
            <div className="flex items-center gap-2">
              {card.default ? (
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded font-semibold">Varsayılan</span>
              ) : (
                <button onClick={() => setDefaultCard(card.id)}
                  className="text-xs text-blue-600 hover:text-blue-800 font-semibold">Varsayılan Yap</button>
              )}
              <button onClick={() => removeCard(card.id)}
                className="text-xs text-red-500 hover:text-red-700 font-semibold">Sil</button>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-4 mb-8">
        <h2 className="text-lg font-semibold">Diğer Ödeme Yöntemleri</h2>
        {methods.map(m => (
          <div key={m.id} className="border rounded-lg p-4 flex items-center gap-4">
            <div className="w-14 h-9 rounded bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-600">
              {m.type === 'iban' ? 'IBAN' : m.type === 'mobile' ? 'MOB' : ''}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-sm">{m.label}</p>
              <p className="text-xs text-gray-500 font-mono">{m.details}</p>
            </div>
            <button className="text-xs text-red-500 hover:text-red-700 font-semibold">Sil</button>
          </div>
        ))}
      </div>

      <button onClick={() => setShowAdd(!showAdd)}
        className="border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-lg p-4 w-full text-center text-sm text-gray-500 hover:text-blue-600 font-semibold transition-colors">
        + Yeni Kart Ekle
      </button>

      {showAdd && (
        <div className="mt-4 border rounded-lg p-5 bg-gray-50">
          <h3 className="font-semibold mb-4">Yeni Kart Bilgileri</h3>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className="text-xs font-semibold text-gray-500 block mb-1">Kart Üzerindeki İsim</label>
              <input type="text" className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Ad Soyad" />
            </div>
            <div className="sm:col-span-2">
              <label className="text-xs font-semibold text-gray-500 block mb-1">Kart Numarası</label>
              <input type="text" className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="1234 5678 9012 3456" />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">Son Kullanma</label>
              <input type="text" className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="AA / YY" />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-500 block mb-1">CVC</label>
              <input type="text" className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="123" />
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">Kaydet</button>
            <button onClick={() => setShowAdd(false)} className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">İptal</button>
          </div>
        </div>
      )}
    </div>
  );
}
