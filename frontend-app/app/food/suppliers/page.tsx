"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function SuppliersPage() {
  const router = useRouter();
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    fetch(`${API}/food/suppliers`)
      .then(r => r.json())
      .then(d => setSuppliers(Array.isArray(d) ? d : d?.value || []))
      .catch(() => {});
  }, []);

  const types = ["", "producer", "home_chef", "commercial"];
  const typeLabels: Record<string,string> = { "":"Tümü","producer":"🌿 Üretici","home_chef":"🏠 Ev Yemekçisi","commercial":"🏭 Ticari" };
  const filtered = filter ? suppliers.filter(s => s.supplier_type === filter) : suppliers;

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 32px"}}>
        <span onClick={()=>router.push("/food")} style={{cursor:"pointer",fontSize:13,color:"#5A7499",fontWeight:500}}>← Yemek</span>
      </nav>

      <div style={{padding:"24px 32px",maxWidth:800,margin:"0 auto"}}>
        <h1 style={{fontSize:22,fontWeight:700,letterSpacing:-0.8,marginBottom:8}}>Tüm Tedarikçiler</h1>
        <div style={{display:"flex",gap:8,marginBottom:20,flexWrap:"wrap"}}>
          {types.map(t => (
            <button key={t} onClick={()=>setFilter(t)} style={{padding:"6px 14px",background:filter===t?"#4A7FD4":"#fff",color:filter===t?"#fff":"#5A7499",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,fontWeight:500,cursor:"pointer",fontFamily:"inherit"}}>{typeLabels[t]}</button>
          ))}
        </div>

        {filtered.map((s: any) => (
          <div key={s.id} className="biz-card" onClick={()=>router.push(`/food/suppliers/${s.slug}`)} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:16,marginBottom:12,cursor:"pointer"}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"start"}}>
              <div>
                <div style={{fontSize:16,fontWeight:600}}>{s.company_name}</div>
                <div style={{fontSize:12,color:"#8FAAC8",marginTop:4}}>{typeLabels[s.supplier_type] || s.supplier_type}</div>
                <div style={{fontSize:12,color:"#5A7499",marginTop:6}}>
                  {s.city && <span>{s.city}</span>}
                  {s.rating > 0 && <span style={{marginLeft:12}}>⭐ {s.rating.toFixed(1)}</span>}
                  {s.product_count !== undefined && <span style={{marginLeft:12}}>📦 {s.product_count} ürün</span>}
                </div>
              </div>
              <div style={{fontSize:12,color:"#4A7FD4",fontWeight:600}}>İncele →</div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
