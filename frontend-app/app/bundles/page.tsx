"use client";

export default function BundlesPage() {
  const bundles = [
    { name: "Oyun Seti", items: "Konsol + Kulaklık + 2 Oyun", price: "₺15.999", original: "₺19.997", discount: "%20" },
    { name: "Ev Ofis Paketi", items: "Masa + Sandalye + Lamba", price: "₺7.499", original: "₺9.997", discount: "%25" },
    { name: "Spor Paketi", items: "Spor Ayakkabı + Eşofman + Mat", price: "₺3.299", original: "₺4.497", discount: "%27" },
    { name: "Cilt Bakım Seti", items: "Serum + Nemlendirici + Güneş Kremi", price: "₺1.299", original: "₺1.797", discount: "%28" },
  ];

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Fırsat Paketleri</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {bundles.map((b) => (
          <div key={b.name} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
            <div className="inline-block bg-red-100 text-red-700 text-xs font-semibold px-2 py-0.5 rounded mb-3">{b.discount} İndirim</div>
            <h3 className="font-semibold text-gray-900">{b.name}</h3>
            <p className="text-sm text-gray-500 mt-1">{b.items}</p>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-lg font-bold text-gray-900">{b.price}</span>
              <span className="text-sm text-gray-400 line-through">{b.original}</span>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
