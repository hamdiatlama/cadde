"use client";

export default function PreOrderPage() {
  const items = [
    { name: "PlayStation 6", date: "15 Temmuz 2026", price: "₺24.999", status: "Ön Sipariş Verildi" },
    { name: "iPhone 18 Pro", date: "Eylül 2026", price: "₺89.999", status: "Bekleniyor" },
    { name: "Samsung Galaxy S28", date: "Şubat 2027", price: "₺45.999", status: "Ön Sipariş Verildi" },
  ];

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Ön Siparişlerim</h1>
      <div className="space-y-4">
        {items.map((item) => (
          <div key={item.name} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">{item.name}</div>
              <div className="text-sm text-gray-500">Tahmini Teslimat: {item.date}</div>
              <div className="text-xs text-gray-400 mt-1">{item.price}</div>
            </div>
            <span className="text-xs font-medium text-blue-700 bg-blue-50 px-3 py-1 rounded-full">{item.status}</span>
          </div>
        ))}
      </div>
    </main>
  );
}
