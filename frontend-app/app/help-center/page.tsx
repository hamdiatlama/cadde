"use client";

export default function HelpCenterPage() {
  const articles = [
    { title: "Siparişimi nasıl takip ederim?", category: "Sipariş" },
    { title: "İade süreci nasıl işler?", category: "İade" },
    { title: "Hediye çeki nasıl kullanılır?", category: "Hediye Çeki" },
    { title: "Satıcı hesabı nasıl açılır?", category: "Satıcı" },
    { title: "Ödeme seçenekleri nelerdir?", category: "Ödeme" },
    { title: "Kargo ücreti ne kadar?", category: "Kargo" },
    { title: "Üyelik bilgilerimi nasıl güncellerim?", category: "Hesap" },
    { title: "Güvenlik ve gizlilik politikası", category: "Güvenlik" },
  ];

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Yardım Merkezi</h1>
      <p className="text-sm text-gray-500 mb-6">Sık sorulan sorular ve yardım dokümanları.</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {articles.map((a) => (
          <div key={a.title} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
            <span className="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-0.5 rounded">{a.category}</span>
            <h3 className="font-medium text-gray-900 text-sm mt-2">{a.title}</h3>
          </div>
        ))}
      </div>
    </main>
  );
}
