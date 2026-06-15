from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.core.auth import get_current_user
from src.modules.user.models import User
from src.modules.seller.models import Seller
from src.modules.cargo.schemas import (
    CompanyCreate, CompanyUpdate, CompanyResponse,
    BranchCreate, BranchUpdate, BranchResponse,
    CourierCreate, CourierUpdate, CourierResponse,
    ShipmentCreate, ShipmentUpdate, ShipmentResponse,
    TrackingCreate, TrackingResponse,
    PricingCreate, PricingUpdate, PricingResponse,
    ServiceAreaCreate, ServiceAreaUpdate, ServiceAreaResponse,
    AgreementCreate, AgreementResponse, PriceQuoteRequest,
    ProductShippingCreate, ProductShippingResponse,
    DeliverySurveyCreate, DeliverySurveyResponse,
    DeliveryConfirmRequest, ShipmentPublicResponse,
    ReturnRequestCreate, ReturnRequestResponse,
)
from src.modules.cargo.service import CargoService

router = APIRouter(prefix="/cargo", tags=["cargo"])


def _svc(db: AsyncSession = Depends(get_db)) -> CargoService:
    return CargoService(db)


# --- Kargo Firması (Company) CRUD ---

@router.post("/companies", response_model=CompanyResponse)
async def register_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    existing = await svc.get_my_company(user.id)
    if existing:
        raise HTTPException(400, "Zaten bir kargo firmanız var")
    comp = await svc.register(user.id, data)
    await db.commit()
    return comp


@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    comp = await svc.update_company(company_id, data, user.id)
    if not comp:
        raise HTTPException(404, "Firma bulunamadı veya yetkiniz yok")
    await db.commit()
    return comp


@router.get("/companies/me", response_model=CompanyResponse | None)
async def my_company(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    return await svc.get_my_company(user.id)


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    comp = await svc.get_company(company_id)
    if not comp or not comp.is_active:
        raise HTTPException(404, "Firma bulunamadı")
    return comp


@router.get("/companies", response_model=list[CompanyResponse])
async def list_companies(
    city: str = None,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_companies(city)


# --- Şube (Branch) CRUD ---

@router.post("/companies/{company_id}/branches", response_model=BranchResponse)
async def add_branch(
    company_id: int,
    data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    branch = await svc.add_branch(company_id, data, user.id)
    if not branch:
        raise HTTPException(404, "Firma bulunamadı veya yetkiniz yok")
    await db.commit()
    return branch


@router.put("/branches/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: int,
    data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    branch = await svc.update_branch(branch_id, data, user.id)
    if not branch:
        raise HTTPException(404, "Şube bulunamadı veya yetkiniz yok")
    await db.commit()
    return branch


@router.get("/companies/{company_id}/branches", response_model=list[BranchResponse])
async def list_branches(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_branches(company_id)


# --- Kurye (Courier) CRUD ---

@router.post("/companies/{company_id}/couriers", response_model=CourierResponse)
async def add_courier(
    company_id: int,
    data: CourierCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    courier = await svc.add_courier(company_id, data, user.id)
    if not courier:
        raise HTTPException(404, "Firma bulunamadı veya yetkiniz yok")
    await db.commit()
    return courier


@router.put("/couriers/{courier_id}", response_model=CourierResponse)
async def update_courier(
    courier_id: int,
    data: CourierUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    courier = await svc.update_courier(courier_id, data, user.id)
    if not courier:
        raise HTTPException(404, "Kurye bulunamadı veya yetkiniz yok")
    await db.commit()
    return courier


@router.get("/companies/{company_id}/couriers", response_model=list[CourierResponse])
async def list_couriers(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_couriers(company_id)


@router.get("/companies/{company_id}/couriers/available", response_model=list[CourierResponse])
async def list_available_couriers(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_available_couriers(company_id)


# --- Fiyatlandırma (Pricing) ---

@router.post("/companies/{company_id}/pricing", response_model=PricingResponse)
async def add_pricing(
    company_id: int,
    data: PricingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    tier = await svc.add_pricing(company_id, data, user.id)
    if not tier:
        raise HTTPException(404, "Firma bulunamadı veya yetkiniz yok")
    await db.commit()
    return tier


@router.put("/pricing/{tier_id}", response_model=PricingResponse)
async def update_pricing(
    tier_id: int,
    data: PricingUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    tier = await svc.update_pricing(tier_id, data, user.id)
    if not tier:
        raise HTTPException(404, "Fiyatlandırma bulunamadı veya yetkiniz yok")
    await db.commit()
    return tier


@router.get("/companies/{company_id}/pricing", response_model=list[PricingResponse])
async def list_pricing(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_pricing(company_id)


@router.post("/price-quote")
async def price_quote(
    data: PriceQuoteRequest,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    result = await svc.calculate_price(
        data.company_id, data.weight_kg, data.volume_dm3,
        data.from_city, data.to_city, data.is_express,
    )
    if not result:
        raise HTTPException(404, "Bu kriterlere uygun fiyatlandırma bulunamadı")
    return result


# --- Hizmet Bölgeleri (Service Areas) ---

@router.post("/companies/{company_id}/service-areas", response_model=ServiceAreaResponse)
async def add_service_area(
    company_id: int,
    data: ServiceAreaCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    area = await svc.add_service_area(company_id, data, user.id)
    if not area:
        raise HTTPException(404, "Firma bulunamadı veya yetkiniz yok")
    await db.commit()
    return area


@router.put("/service-areas/{area_id}", response_model=ServiceAreaResponse)
async def update_service_area(
    area_id: int,
    data: ServiceAreaUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    area = await svc.update_service_area(area_id, data, user.id)
    if not area:
        raise HTTPException(404, "Bölge bulunamadı veya yetkiniz yok")
    await db.commit()
    return area


@router.get("/companies/{company_id}/service-areas", response_model=list[ServiceAreaResponse])
async def list_service_areas(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_service_areas(company_id)


# --- Gönderi (Shipment) ---

@router.post("/shipments", response_model=ShipmentResponse, status_code=201)
async def create_shipment(
    data: ShipmentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    shipment = await svc.create_shipment(data, user.id)
    await db.commit()
    return shipment


@router.put("/shipments/{shipment_id}", response_model=ShipmentResponse)
async def update_shipment(
    shipment_id: int,
    data: ShipmentUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    shipment = await svc.update_shipment(shipment_id, data, user.id)
    if not shipment:
        raise HTTPException(404, "Gönderi bulunamadı")
    await db.commit()
    return shipment


@router.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    shipment = await svc.get_shipment(shipment_id)
    if not shipment:
        raise HTTPException(404, "Gönderi bulunamadı")
    return shipment


@router.get("/shipments/tracking/{tracking_no}", response_model=ShipmentResponse)
async def track_by_no(
    tracking_no: str,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    shipment = await svc.get_shipment_by_tracking(tracking_no)
    if not shipment:
        raise HTTPException(404, "Gönderi bulunamadı")
    return shipment


@router.get("/companies/{company_id}/shipments", response_model=list[ShipmentResponse])
async def list_company_shipments(
    company_id: int,
    status: str = None,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.list_company_shipments(company_id, status)


# --- Takip (Tracking) ---

@router.post("/shipments/{shipment_id}/tracking", status_code=201)
async def add_tracking(
    shipment_id: int,
    data: TrackingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    result = await svc.add_tracking(shipment_id, data)
    if not result:
        raise HTTPException(404, "Gönderi bulunamadı")
    await db.commit()
    return result


@router.get("/shipments/{shipment_id}/tracking", response_model=list[TrackingResponse])
async def get_tracking(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.get_tracking(shipment_id)


@router.get("/public/tracking/{tracking_no}")
async def public_tracking(
    tracking_no: str,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    shipment = await svc.get_shipment_by_tracking(tracking_no)
    if not shipment:
        raise HTTPException(404, "Gönderi bulunamadı")
    tracking = await svc.get_tracking(shipment.id)
    survey = await svc.get_survey(shipment.id)
    return {
        "tracking_no": shipment.tracking_no,
        "status": shipment.status,
        "sender_name": shipment.sender_name,
        "sender_city": shipment.sender_city,
        "recipient_name": shipment.recipient_name,
        "recipient_city": shipment.recipient_city,
        "is_fragile": shipment.is_fragile,
        "sensitivity_note": shipment.sensitivity_note,
        "estimated_delivery": shipment.estimated_delivery_date,
        "steps": [
            {"status": t.status, "location": t.location_name,
             "notes": t.notes, "time": t.created_at}
            for t in tracking
        ],
        "survey": {
            "delivered_on_time": survey.delivered_on_time,
            "package_condition": survey.package_condition,
            "is_package_damaged": survey.is_package_damaged,
            "is_package_opened": survey.is_package_opened,
            "satisfaction_score": survey.satisfaction_score,
        } if survey else None,
    }


# --- Satıcı-Kargo Anlaşmaları (Seller Agreements) ---

@router.post("/agreements", response_model=AgreementResponse)
async def add_agreement(
    data: AgreementCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(400, "Satıcı hesabınız bulunmuyor")
    agreement = await svc.add_agreement(seller.id, data)
    await db.commit()
    comp = await svc.get_company(data.company_id)
    return {
        "id": agreement.id,
        "seller_id": agreement.seller_id,
        "company_id": agreement.company_id,
        "company_name": comp.company_name if comp else "",
        "is_preferred": agreement.is_preferred,
        "contract_start": agreement.contract_start,
        "contract_end": agreement.contract_end,
        "negotiated_price_factor": agreement.negotiated_price_factor,
        "notes": agreement.notes,
        "is_active": agreement.is_active,
    }


@router.delete("/agreements/{agreement_id}")
async def remove_agreement(
    agreement_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(400, "Satıcı hesabınız bulunmuyor")
    ok = await svc.remove_agreement(agreement_id, seller.id)
    if not ok:
        raise HTTPException(404, "Anlaşma bulunamadı")
    await db.commit()
    return {"ok": True}


@router.get("/agreements/mine", response_model=list[AgreementResponse])
async def my_agreements(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return []
    return await svc.list_seller_agreements(seller.id)


# --- Ürün-Kargo Ayarları (Product Shipping) ---

@router.post("/product-shipping", response_model=ProductShippingResponse)
async def set_product_shipping(
    data: ProductShippingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(400, "Satıcı hesabınız bulunmuyor")
    result = await svc.set_product_shipping(seller.id, data)
    await db.commit()
    return result


@router.get("/product-shipping/{product_id}", response_model=ProductShippingResponse | None)
async def get_product_shipping(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(400, "Satıcı hesabınız bulunmuyor")
    return await svc.get_product_shipping(seller.id, product_id)


@router.get("/my-products/shipping", response_model=list[ProductShippingResponse])
async def list_my_product_shipping(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return []
    return await svc.list_my_product_shipping(seller.id)


# --- QR Teslimat Onayı ---

@router.post("/shipments/{shipment_id}/generate-delivery-code")
async def generate_delivery_code(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    code = await svc.generate_delivery_code(shipment_id)
    if not code:
        raise HTTPException(404, "Gönderi bulunamadı")
    await db.commit()
    return {"delivery_code": code, "qr_content": f"CARGO-DELIVER-{code}"}


@router.post("/delivery/confirm")
async def confirm_delivery(
    data: DeliveryConfirmRequest,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    result = await svc.confirm_delivery(data.delivery_code, data.delivery_note)
    if "error" in result:
        raise HTTPException(404, result["error"])
    await db.commit()
    return result


@router.post("/delivery/reject")
async def reject_delivery(
    data: DeliveryConfirmRequest,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    result = await svc.reject_delivery(data.delivery_code, data.delivery_note)
    if "error" in result:
        raise HTTPException(404, result["error"])
    await db.commit()
    return result


# --- Teslimat Memnuniyet Anketi ---

@router.post("/shipments/{shipment_id}/survey", response_model=DeliverySurveyResponse)
async def submit_delivery_survey(
    shipment_id: int,
    data: DeliverySurveyCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    survey = await svc.submit_survey(shipment_id, user.id, data)
    if not survey:
        raise HTTPException(400, "Anket daha önce doldurulmuş veya gönderi bulunamadı")
    await db.commit()
    return survey


@router.get("/shipments/{shipment_id}/survey", response_model=DeliverySurveyResponse | None)
async def get_delivery_survey(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    return await svc.get_survey(shipment_id)


# --- İade Talebi (30 dk test süresi) ---

@router.post("/shipments/{shipment_id}/return-request")
async def create_return_request(
    shipment_id: int,
    data: ReturnRequestCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Teslimattan sonra 30 dk içinde iade talebi. Kötü niyetli alıcılar otomatik tespit edilir."""
    svc = CargoService(db)
    result = await svc.create_return_request(shipment_id, user.id, data)
    if "error" in result:
        if result.get("fraud_status") == "blocked":
            raise HTTPException(403, result["error"])
        raise HTTPException(400, result["error"])
    await db.commit()
    return result


@router.get("/shipments/{shipment_id}/return-request")
async def get_return_request(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = CargoService(db)
    result = await svc.get_return_request(shipment_id)
    if not result:
        raise HTTPException(404, "İade talebi bulunamadı")
    return result


# --- Kargo Firması Hasar/İade Bildirimleri ---

@router.get("/companies/{company_id}/claims")
async def list_company_claims(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = CargoService(db)
    return await svc.list_company_claims(company_id, user.id)


# --- Teslimat Başarısız / Şubede Bekleme ---

@router.post("/shipments/{shipment_id}/undelivered")
async def mark_undelivered(
    shipment_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    """Kurye adreste bulamadı, şubeye götürüldü (2 gün bekler)"""
    svc = CargoService(db)
    result = await svc.mark_undelivered(
        shipment_id, data.get("reason", "Adreste bulunamadı"),
        data.get("branch_id"), 0,
    )
    if "error" in result:
        raise HTTPException(400, result["error"])
    await db.commit()
    return result


@router.post("/shipments/{shipment_id}/extend-pickup")
async def extend_pickup(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Müşteri 'ben alacağım' derse 1 gün eklenir"""
    svc = CargoService(db)
    result = await svc.extend_pickup(shipment_id, user.id)
    if "error" in result:
        raise HTTPException(400, result["error"])
    await db.commit()
    return result


@router.post("/shipments/{shipment_id}/auto-return-expired")
async def auto_return_expired(
    shipment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Bekleme süresi dolan gönderileri otomatik iade et"""
    svc = CargoService(db)
    result = await svc.auto_return_expired(shipment_id)
    if "error" in result:
        raise HTTPException(400, result["error"])
    await db.commit()
    return result


# --- Satıcı Askıya Alma Sistemi (tüm satıcı/üreticiler için) ---

@router.get("/seller/suspension")
async def check_seller_suspension(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from src.modules.seller.models import Seller
    r = await db.execute(select(Seller).where(Seller.user_id == user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return {"is_suspended": False}
    svc = CargoService(db)
    result = await svc.check_seller_suspension(seller.id)
    return result or {"is_suspended": False}
