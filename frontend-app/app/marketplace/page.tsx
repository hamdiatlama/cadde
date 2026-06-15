"use client";

export default function MarketplacePage() {
  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Pazaryeri</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-blue-700 text-lg font-bold">S</span>
          </div>
          <h2 className="font-semibold text-gray-900 mb-1">Çoklu Satıcı Sepeti</h2>
          <p className="text-sm text-gray-500">Farklı satıcılardan ürünleri tek sepette birleştirin.</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-green-700 text-lg font-bold">B</span>
          </div>
          <h2 className="font-semibold text-gray-900 mb-1">Satıcı Başvurusu</h2>
          <p className="text-sm text-gray-500">Mağazanızı açın ve satışa başlayın.</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-purple-700 text-lg font-bold">Ö</span>
          </div>
          <h2 className="font-semibold text-gray-900 mb-1">Ön Sipariş</h2>
          <p className="text-sm text-gray-500">Çıkacak ürünleri önceden sipariş verin.</p>
        </div>
      </div>
      <section>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Öne Çıkan Satıcılar</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {["TeknoMarket", "ModaDünyası", "EvimGüzel", "KitapKurdu"].map((name) => (
            <div key={name} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="font-medium text-gray-900">{name}</div>
              <div className="text-sm text-gray-500 mt-1">4.5 ★</div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
