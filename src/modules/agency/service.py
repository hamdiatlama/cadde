from src.modules.agency.repository import AgencyRepository


class AgencyService:
    def __init__(self, repo: AgencyRepository):
        self.repo = repo

    async def register_agency(self, user_id: int, data: dict):
        existing = await self.repo.get_agency_by_user(user_id)
        if existing:
            raise ValueError("Bu kullanıcının zaten bir acentelik kaydı var")
        data["user_id"] = user_id
        return await self.repo.create_agency(data)

    async def request_authorization(self, agency_id: int, domain: str, provider_id: int, provider_name: str, commission_split: float = 0):
        existing = await self.repo.list_authorizations(agency_id, domain, provider_id)
        if existing:
            raise ValueError("Bu firma için zaten bir yetkilendirme talebi var")
        data = {
            "agency_id": agency_id,
            "domain": domain,
            "provider_id": provider_id,
            "provider_name": provider_name,
            "commission_split": commission_split,
        }
        return await self.repo.create_authorization(data)

    async def get_authorized_providers(self, agency_id: int, domain: str = None):
        return await self.repo.list_authorizations(agency_id=agency_id, domain=domain, status="approved")


def get_agency_service(repo=Depends(get_agency_repo)) -> AgencyService:
    return AgencyService(repo)
