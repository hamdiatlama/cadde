"use client";
import { useRouter, useParams } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function SupplierPage() {
  const { slug } = useParams();
  const router = useRouter();
  const [supplier, setSupplier] = useState<any>(null);

  useEffect(() => {
    if (!slug) return;
    fetch(`${API}/food/suppliers/page/${slug}`)
      .then(r => r.json())
      .then(d => setSupplier(d))
      .catch(() => {});
  }, [slug]);

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 32px"}}>
        <span onClick={()=>router.push("/food/suppliers")} style={{cursor:"pointer",fontSize:13,color:"#5A7499",fontWeight:500}}>← Tedarikçiler</span>
      </nav>

      <div style={{padding:"24px 32px",maxWidth:720,margin:"0 auto"}}>
        {!supplier ? <p>Yükleniyor...</p> : (
          <>
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:20,marginBottom:20}}>
              <div style={{display:"flex",alignItems:"center",gap:16}}>
                {supplier.logo_url && <img src={supplier.logo_url} style={{width:60,height:60,borderRadius:10,objectFit:"cover",background:"#EEF4FF"}}/>}
                <div>
                  <h1 style={{fontSize:22,fontWeight:700}}>{supplier.company_name}</h1>
                  <div style={{fontSize:12,color:"#8FAAC8",marginTop:4}}>
                    {supplier.supplier_type === "home_chef" ? "🏠 Ev Yemekçisi" : supplier.supplier_type === "producer" ? "🌿 Üretici" : "🏭 Ticari Tedarikçi"}
                    {supplier.is_verified && <span style={{marginLeft:8,color:"#22C55E"}}>✅ Doğrulanmış</span>}
                  </div>
                  <div style={{fontSize:12,color:"#5A7499",marginTop:6}}>
                    {supplier.city && <span>{supplier.city} · </span>}
                    ⭐ {supplier.rating?.toFixed(1) || "0.0"}
                  </div>
                </div>
              </div>
              {supplier.description && <p style={{fontSize:13,color:"#5A7499",marginTop:14,lineHeight:1.6}}>{supplier.description}</p>}
            </div>

            <h2 style={{fontSize:16,fontWeight:600,marginBottom:12}}>📦 Ürünler</h2>
            {(!supplier.products || supplier.products.length === 0) ? (
              <p style={{color:"#8FAAC8",fontSize:13,textAlign:"center",padding:20}}>Henüz ürün eklenmemiş</p>
            ) : (
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
                {supplier.products.map((p: any) => (
                  <div key={p.id} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:14}}>
                    <div style={{fontSize:14,fontWeight:600}}>{p.name}</div>
                    <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>{p.category}</div>
                    <div style={{fontSize:16,fontWeight:700,color:"#4A7FD4",marginTop:8}}>₺{p.price_per_unit || p.price}/{p.unit || "adet"}</div>
                    {p.is_organic && <span style={{display:"inline-block",marginTop:4,fontSize:10,background:"#DCFCE7",color:"#16A34A",padding:"2px 6px",borderRadius:4,fontWeight:600}}>Organik</span>}
                  </div>
                ))}
              </div>
            )}

            {supplier.transparency_score !== undefined && (
              <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:16,marginTop:20}}>
                <h2 style={{fontSize:14,fontWeight:600,marginBottom:8}}>📊 Şeffaflık Puanı</h2>
                <div style={{fontSize:28,fontWeight:700,color:"#4A7FD4"}}>{supplier.transparency_score}%</div>
                <div style={{fontSize:11,color:"#8FAAC8",marginTop:4}}>Toplam puan: {supplier.total_points}</div>
              </div>
            )}

            {supplier.restaurants?.length > 0 && (
              <div style={{marginTop:20}}>
                <h2 style={{fontSize:14,fontWeight:600,marginBottom:12}}>🏪 Tedarik Ettiği Restoranlar</h2>
                {supplier.restaurants.map((r: any) => (
                  <div key={r.id} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:10,padding:12,marginBottom:8,cursor:"pointer"}} onClick={()=>router.push(`/food/${r.id}`)}>
                    <div style={{display:"flex",justifyContent:"space-between"}}>
                      <span style={{fontSize:13,fontWeight:600}}>{r.name}</span>
                      <span style={{fontSize:11,color:"#8FAAC8"}}>{r.is_preferred ? "⭐ Tercih Edilen" : ""}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}
