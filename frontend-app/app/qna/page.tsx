"use client";
import { useState } from "react";

export default function QnAPage() {
  const [question, setQuestion] = useState("");
  const [questions, setQuestions] = useState([
    { q: "Bu ürünün garantisi var mı?", a: "Evet, 2 yıl garantilidir.", author: "Satıcı" },
    { q: "Pil ömrü ne kadar?", a: "Ortalama 8 saat kullanım süresi vardır.", author: "Satıcı" },
  ]);

  function handleAsk() {
    if (!question.trim()) return;
    setQuestions([...questions, { q: question, a: "Henüz yanıtlanmadı.", author: "Siz" }]);
    setQuestion("");
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Ürün Soru & Cevap</h1>
      <div className="mb-8 flex gap-2">
        <input
          type="text" value={question} onChange={(e) => setQuestion(e.target.value)}
          placeholder="Bir soru sorun..."
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button onClick={handleAsk} className="bg-blue-600 text-white rounded-lg px-4 text-sm font-medium hover:bg-blue-700 transition-colors">
          Sor
        </button>
      </div>
      <div className="space-y-4">
        {questions.map((item, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <p className="font-medium text-gray-900 text-sm">{item.q}</p>
              <span className="text-xs text-gray-400">{item.author}</span>
            </div>
            <p className="text-sm text-gray-600">{item.a}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
