"use client";

export default function CompliancePage() {
  return (
    <main className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Uyumluluk Paneli</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="font-semibold text-gray-900 text-sm">MAP Politikaları</h2>
          <p className="text-xs text-gray-500 mt-1">3 politika ihlal edildi</p>
          <span className="text-xs text-red-600 font-medium mt-2 inline-block">İncele →</span>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="font-semibold text-gray-900 text-sm">Sertifikalar</h2>
          <p className="text-xs text-gray-500 mt-1">12 sertifika aktif</p>
          <span className="text-xs text-blue-600 font-medium mt-2 inline-block">Görüntüle →</span>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="font-semibold text-gray-900 text-sm">Geri Çağırmalar</h2>
          <p className="text-xs text-gray-500 mt-1">1 ürün geri çağrıldı</p>
          <span className="text-xs text-orange-600 font-medium mt-2 inline-block">Detay →</span>
        </div>
      </div>
      <section>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Son İhlaller</h2>
        <div className="bg-white border border-gray-200 rounded-lg">
          {["Ürün #1234 - MAP altı fiyatlandırma", "Ürün #5678 - Yetkisiz satıcı", "Ürün #9012 - Yanıltıcı görsel"].map((item, i) => (
            <div key={i} className="px-4 py-3 border-b border-gray-100 last:border-b-0 text-sm text-gray-700">{item}</div>
          ))}
        </div>
      </section>
    </main>
  );
}
