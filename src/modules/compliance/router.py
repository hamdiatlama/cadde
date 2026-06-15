from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.compliance.repository import (
    MapPolicyRepository, CounterfeitRepository, ProductComplianceRepository,
    ProductRecallRepository, PolicyViolationRepository,
)

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.post("/map/policies", status_code=201)
async def set_map_policy(product_id: int, min_advertised_price: float,
                         db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = MapPolicyRepository(db)
    mp = await repo.set_policy(current_user.id, product_id, min_advertised_price)
    await db.commit()
    return {"id": mp.id, "product_id": mp.product_id, "min_advertised_price": mp.min_advertised_price}


@router.post("/map/check/{product_id}")
async def check_map_violation(product_id: int, price: float = Query(...),
                              db: AsyncSession = Depends(get_db)):
    repo = MapPolicyRepository(db)
    return await repo.check_violation(product_id, price)


@router.get("/map/violations")
async def list_map_violations(db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    repo = MapPolicyRepository(db)
    return await repo.list_violations()


@router.post("/counterfeit/report", status_code=201)
async def report_counterfeit(product_id: int, description: str = None, evidence_url: str = None,
                             db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CounterfeitRepository(db)
    cr = await repo.report(product_id, current_user.id, description=description, evidence_url=evidence_url)
    await db.commit()
    return {"id": cr.id, "status": cr.status}


@router.get("/counterfeit/reports")
async def list_counterfeit_reports(db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)):
    repo = CounterfeitRepository(db)
    return await repo.list_reports()


@router.put("/counterfeit/reports/{report_id}/resolve")
async def resolve_counterfeit_report(report_id: int, db: AsyncSession = Depends(get_db),
                                     current_user: User = Depends(get_current_user)):
    repo = CounterfeitRepository(db)
    cr = await repo.resolve_report(report_id)
    if not cr:
        raise HTTPException(404, "Report not found")
    await db.commit()
    return {"id": cr.id, "status": cr.status}


@router.post("/compliance/certificates", status_code=201)
async def add_certificate(product_id: int, cert_type: str, cert_number: str = None,
                          cert_file_url: str = None, issued_at: str = None, expires_at: str = None,
                          db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ProductComplianceRepository(db)
    pc = await repo.add_certificate(product_id, cert_type=cert_type, cert_number=cert_number,
                                    cert_file_url=cert_file_url, issued_at=issued_at, expires_at=expires_at)
    await db.commit()
    return {"id": pc.id, "cert_type": pc.cert_type}


@router.get("/compliance/certificates/{product_id}")
async def list_certificates(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductComplianceRepository(db)
    return await repo.list_certificates(product_id)


@router.post("/recalls", status_code=201)
async def create_recall(product_id: int, reason: str, risk_level: str = None,
                        affected_batch: str = None, action_taken: str = None,
                        db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ProductRecallRepository(db)
    pr = await repo.create_recall(product_id, reason, risk_level=risk_level,
                                  affected_batch=affected_batch, action_taken=action_taken)
    await db.commit()
    return {"id": pr.id, "status": pr.status}


@router.get("/recalls/active")
async def list_active_recalls(db: AsyncSession = Depends(get_db)):
    repo = ProductRecallRepository(db)
    return await repo.list_active()


@router.put("/recalls/{recall_id}/resolve")
async def resolve_recall(recall_id: int, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    repo = ProductRecallRepository(db)
    pr = await repo.resolve_recall(recall_id)
    if not pr:
        raise HTTPException(404, "Recall not found")
    await db.commit()
    return {"id": pr.id, "status": pr.status}


@router.post("/violations", status_code=201)
async def report_violation(seller_id: int, violation_type: str, description: str = None,
                           evidence: str = None, penalty: str = None,
                           db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = PolicyViolationRepository(db)
    pv = await repo.report_violation(seller_id, violation_type, description=description,
                                     evidence=evidence, penalty=penalty)
    await db.commit()
    return {"id": pv.id, "status": pv.status}


@router.get("/violations")
async def list_violations(seller_id: int = None, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    repo = PolicyViolationRepository(db)
    return await repo.list_by_seller(seller_id)


@router.put("/violations/{violation_id}/resolve")
async def resolve_violation(violation_id: int, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    repo = PolicyViolationRepository(db)
    pv = await repo.resolve(violation_id)
    if not pv:
        raise HTTPException(404, "Violation not found")
    await db.commit()
    return {"id": pv.id, "status": pv.status}
