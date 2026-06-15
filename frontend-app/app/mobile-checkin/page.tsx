"use client";
import { useState } from "react";

const MOCK_CHECKINS = [
  { id:1, guest:"Ali Yılmaz", room:"205", status:"pending", time:"14:30", idVerified:false },
  { id:2, guest:"Ayşe Demir", room:"312", status:"pending", time:"15:00", idVerified:false },
  { id:3, guest:"Mehmet Kaya", room:"108", status:"verified", time:"12:15", idVerified:true },
  { id:4, guest:"Zeynep Öz", room:"421", status:"completed", time:"11:00", idVerified:true },
];

const MOCK_KEYS = [
  { id:1, guest:"Ali Yılmaz", room:"205", status:"active", validUntil:"2026-06-16 14:30", qr:"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=key001" },
  { id:2, guest:"Ayşe Demir", room:"312", status:"active", validUntil:"2026-06-16 15:00", qr:"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=key002" },
  { id:3, guest:"Mehmet Kaya", room:"108", status:"expired", validUntil:"2026-06-14 12:15", qr:"" },
];

const MOCK_EARLY = [
  { id:1, guest:"Ali Yılmaz", room:"205", time:"10:00", status:"pending" },
  { id:2, guest:"Fatma Can", room:"118", time:"09:30", status:"approved" },
];

const MOCK_LATE = [
  { id:1, guest:"Ayşe Demir", room:"312", time:"15:00", status:"pending", fee:50 },
  { id:2, guest:"Mehmet Kaya", room:"108", time:"14:00", status:"approved", fee:0 },
];

export default function MobileCheckinPage() {
  const [tab, setTab] = useState("checkins");
  const [selectedKey, setSelectedKey] = useState<number|null>(null);
  const [showQR, setShowQR] = useState<number|null>(null);

  const statusStyle = (s: string) => {
    const m: Record<string,string> = {pending:"#F59E0B",verified:"#3B82F6",completed:"#10B981",active:"#10B981",expired:"#EF4444",revoked:"#8B5CF6",approved:"#10B981"};
    return { background:m[s]||"#8FAAC8", color:"#fff", fontSize:11, fontWeight:600, padding:"3px 10px", borderRadius:20, textTransform:"capitalize" as const };
  };

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>
      <div style={{maxWidth:1200,margin:"0 auto",padding:"24px 32px"}}>
        <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:24}}>
          <i className="ti ti-device-mobile" style={{fontSize:24,color:"#4A7FD4"}}/>
          <h1 style={{fontSize:22,fontWeight:700,letterSpacing:-0.5}}>Mobile Check-in & Dijital Anahtar</h1>
        </div>

        {/* TABS */}
        <div style={{display:"flex",gap:4,marginBottom:24,background:"#fff",borderRadius:8,padding:4,border:"1px solid #D6E4FA",width:"fit-content"}}>
          {[
            {key:"checkins",icon:"ti-clipboard-list",label:"Giriş Talepleri"},
            {key:"keys",icon:"ti-key",label:"Dijital Anahtarlar"},
            {key:"early",icon:"ti-clock-hour-3",label:"Erken Giriş"},
            {key:"late",icon:"ti-clock-hour-9",label:"Geç Çıkış"},
          ].map(t=>(
            <button key={t.key} onClick={()=>setTab(t.key)} style={{display:"flex",alignItems:"center",gap:6,padding:"8px 16px",borderRadius:6,border:"none",background:tab===t.key?"#4A7FD4":"transparent",color:tab===t.key?"#fff":"#5A7499",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer",transition:"all .15s"}}>
              <i className={`ti ${t.icon}`} style={{fontSize:16}}/>
              {t.label}
            </button>
          ))}
        </div>

        {/* TAB: CHECKINS */}
        {tab==="checkins" && (
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <span style={{fontSize:14,fontWeight:600}}>Mobil Giriş Talepleri</span>
              <span style={{fontSize:12,color:"#8FAAC8"}}>{MOCK_CHECKINS.filter(c=>c.status==="pending").length} bekleyen</span>
            </div>
            {MOCK_CHECKINS.map(c=>(
              <div key={c.id} style={{display:"flex",alignItems:"center",gap:16,padding:"14px 20px",borderBottom:"1px solid #EEF4FF",transition:"background .15s"}} className="hover-row">
                <div style={{width:38,height:38,borderRadius:"50%",background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                  <span style={{fontSize:13,fontWeight:700,color:"#4A7FD4"}}>{c.guest[0]}</span>
                </div>
                <div style={{flex:1}}>
                  <div style={{fontSize:13,fontWeight:600}}>{c.guest}</div>
                  <div style={{fontSize:11,color:"#8FAAC8",marginTop:1}}>Oda {c.room} · {c.time}</div>
                </div>
                <span style={statusStyle(c.status)}>{c.status==="pending"?"Bekliyor":c.status==="verified"?"Doğrulandı":c.status==="completed"?"Tamamlandı":"Bilinmiyor"}</span>
                <div style={{display:"flex",gap:6}}>
                  {c.status==="pending" && (
                    <>
                      <button style={{display:"flex",alignItems:"center",gap:4,padding:"6px 12px",borderRadius:6,border:"none",background:"#10B981",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                        <i className="ti ti-check" style={{fontSize:14}}/> Onayla
                      </button>
                      <button style={{display:"flex",alignItems:"center",gap:4,padding:"6px 12px",borderRadius:6,border:"none",background:"#EF4444",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                        <i className="ti ti-x" style={{fontSize:14}}/> Reddet
                      </button>
                    </>
                  )}
                  {c.status==="verified" && (
                    <button style={{display:"flex",alignItems:"center",gap:4,padding:"6px 12px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                      <i className="ti ti-door" style={{fontSize:14}}/> Giriş Yap
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB: KEYS */}
        {tab==="keys" && (
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
              <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",gap:8}}>
                <i className="ti ti-key" style={{fontSize:16,color:"#4A7FD4"}}/>
                <span style={{fontSize:14,fontWeight:600}}>Dijital Anahtarlar</span>
              </div>
              {MOCK_KEYS.map(k=>(
                <div key={k.id} style={{display:"flex",alignItems:"center",gap:12,padding:"14px 20px",borderBottom:"1px solid #EEF4FF",cursor:"pointer",transition:"background .15s"}}
                  className="hover-row"
                  onClick={()=>{setSelectedKey(k.id); setShowQR(k.id===showQR?null:k.id)}}
                >
                  <div style={{width:36,height:36,borderRadius:8,background:k.status==="active"?"#D1FAE5":"#FEE2E2",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                    <i className="ti ti-key" style={{fontSize:18,color:k.status==="active"?"#10B981":"#EF4444"}}/>
                  </div>
                  <div style={{flex:1}}>
                    <div style={{fontSize:13,fontWeight:600}}>{k.guest}</div>
                    <div style={{fontSize:11,color:"#8FAAC8"}}>Oda {k.room} · Geçerlilik: {k.validUntil}</div>
                  </div>
                  <span style={statusStyle(k.status)}>{k.status}</span>
                  <button onClick={(e)=>{e.stopPropagation(); setShowQR(showQR===k.id?null:k.id)}} style={{display:"flex",alignItems:"center",gap:4,padding:"6px 10px",borderRadius:6,border:"1px solid #D6E4FA",background:"transparent",color:"#4A7FD4",fontFamily:"inherit",fontSize:12,cursor:"pointer"}}>
                    <i className="ti ti-qrcode" style={{fontSize:14}}/>
                  </button>
                </div>
              ))}
            </div>
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",minHeight:300}}>
              {showQR ? (
                <div style={{textAlign:"center",padding:24}}>
                  <div style={{fontSize:13,fontWeight:600,marginBottom:16}}>QR Kod — Oda {MOCK_KEYS.find(k=>k.id===showQR)?.room}</div>
                  <div style={{width:180,height:180,background:"#EEF4FF",border:"2px solid #D6E4FA",borderRadius:12,display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto 16px"}}>
                    <i className="ti ti-qrcode" style={{fontSize:80,color:"#1A2B4A"}}/>
                  </div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>Misafir bu kodu kapı okuyucusuna okutur</div>
                  <button style={{marginTop:12,padding:"8px 20px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                    <i className="ti ti-download" style={{fontSize:14,marginRight:4}}/> İndir
                  </button>
                </div>
              ) : (
                <div style={{textAlign:"center",color:"#8FAAC8"}}>
                  <i className="ti ti-qrcode" style={{fontSize:48,marginBottom:12}}/>
                  <div style={{fontSize:13}}>Bir anahtar seçin</div>
                  <div style={{fontSize:11}}>QR kodu görüntülemek için tıklayın</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB: EARLY CHECKIN */}
        {tab==="early" && (
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <span style={{fontSize:14,fontWeight:600}}>Erken Giriş Talepleri</span>
              <button style={{display:"flex",alignItems:"center",gap:4,padding:"6px 14px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                <i className="ti ti-plus" style={{fontSize:14}}/> Yeni Talep
              </button>
            </div>
            {MOCK_EARLY.map(e=>(
              <div key={e.id} style={{display:"flex",alignItems:"center",gap:16,padding:"14px 20px",borderBottom:"1px solid #EEF4FF"}}>
                <div style={{width:38,height:38,borderRadius:"50%",background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                  <span style={{fontSize:13,fontWeight:700,color:"#4A7FD4"}}>{e.guest[0]}</span>
                </div>
                <div style={{flex:1}}>
                  <div style={{fontSize:13,fontWeight:600}}>{e.guest}</div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>Oda {e.room} · İstenen: {e.time}</div>
                </div>
                <span style={statusStyle(e.status)}>{e.status==="pending"?"Bekliyor":e.status==="approved"?"Onaylandı":"Bilinmiyor"}</span>
                {e.status==="pending" && (
                  <div style={{display:"flex",gap:6}}>
                    <button style={{padding:"6px 12px",borderRadius:6,border:"none",background:"#10B981",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>Onayla</button>
                    <button style={{padding:"6px 12px",borderRadius:6,border:"none",background:"#EF4444",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>Reddet</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* TAB: LATE CHECKOUT */}
        {tab==="late" && (
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <span style={{fontSize:14,fontWeight:600}}>Geç Çıkış Talepleri</span>
              <button style={{display:"flex",alignItems:"center",gap:4,padding:"6px 14px",borderRadius:6,border:"none",background:"#4A7FD4",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                <i className="ti ti-plus" style={{fontSize:14}}/> Yeni Talep
              </button>
            </div>
            {MOCK_LATE.map(l=>(
              <div key={l.id} style={{display:"flex",alignItems:"center",gap:16,padding:"14px 20px",borderBottom:"1px solid #EEF4FF"}}>
                <div style={{width:38,height:38,borderRadius:"50%",background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                  <span style={{fontSize:13,fontWeight:700,color:"#4A7FD4"}}>{l.guest[0]}</span>
                </div>
                <div style={{flex:1}}>
                  <div style={{fontSize:13,fontWeight:600}}>{l.guest}</div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>Oda {l.room} · İstenen: {l.time}{l.fee>0?` · Ek ücret: ${l.fee}`:""}</div>
                </div>
                <span style={statusStyle(l.status)}>{l.status==="pending"?"Bekliyor":l.status==="approved"?"Onaylandı":"Bilinmiyor"}</span>
                {l.status==="pending" && (
                  <div style={{display:"flex",gap:6}}>
                    <button style={{padding:"6px 12px",borderRadius:6,border:"none",background:"#10B981",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>Onayla</button>
                    <button style={{padding:"6px 12px",borderRadius:6,border:"none",background:"#EF4444",color:"#fff",fontFamily:"inherit",fontSize:12,fontWeight:600,cursor:"pointer"}}>Reddet</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
