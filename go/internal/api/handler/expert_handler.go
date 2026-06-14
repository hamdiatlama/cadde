package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type ExpertHandler struct {
	repo *postgres.ExpertRepo
}

func NewExpertHandler(repo *postgres.ExpertRepo) *ExpertHandler {
	return &ExpertHandler{repo: repo}
}

// ── Company ───────────────────────────────────────────────

func (h *ExpertHandler) CreateCompany(w http.ResponseWriter, r *http.Request) {
	var c domain.ExpertCompany
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateCompany(r.Context(), &c); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, c)
}

func (h *ExpertHandler) ListCompanies(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListCompanies(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Expert ────────────────────────────────────────────────

func (h *ExpertHandler) CreateExpert(w http.ResponseWriter, r *http.Request) {
	var e domain.Expert
	if err := json.NewDecoder(r.Body).Decode(&e); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateExpert(r.Context(), &e); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, e)
}

func (h *ExpertHandler) ListExperts(w http.ResponseWriter, r *http.Request) {
	var companyID *int
	if v := r.URL.Query().Get("company_id"); v != "" {
		id, _ := strconv.Atoi(v)
		companyID = &id
	}
	list, err := h.repo.ListExperts(r.Context(), companyID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) GetExpert(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	e, err := h.repo.GetExpert(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, e)
}

// ── Package ───────────────────────────────────────────────

func (h *ExpertHandler) CreatePackage(w http.ResponseWriter, r *http.Request) {
	var p domain.ExpertPackage
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreatePackage(r.Context(), &p); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, p)
}

func (h *ExpertHandler) ListPackages(w http.ResponseWriter, r *http.Request) {
	var companyID *int
	if v := r.URL.Query().Get("company_id"); v != "" {
		id, _ := strconv.Atoi(v)
		companyID = &id
	}
	list, err := h.repo.ListPackages(r.Context(), companyID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Vehicle ───────────────────────────────────────────────

func (h *ExpertHandler) CreateVehicle(w http.ResponseWriter, r *http.Request) {
	var v domain.ExpertVehicle
	if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateVehicle(r.Context(), &v); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, v)
}

func (h *ExpertHandler) ListVehicles(w http.ResponseWriter, r *http.Request) {
	var plate, chassis *string
	if v := r.URL.Query().Get("plate"); v != "" {
		plate = &v
	}
	if v := r.URL.Query().Get("chassis_number"); v != "" {
		chassis = &v
	}
	list, err := h.repo.ListVehicles(r.Context(), plate, chassis)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Report ────────────────────────────────────────────────

func (h *ExpertHandler) CreateReport(w http.ResponseWriter, r *http.Request) {
	var rep domain.ExpertReport
	if err := json.NewDecoder(r.Body).Decode(&rep); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateReport(r.Context(), &rep); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, rep)
}

func (h *ExpertHandler) ListReports(w http.ResponseWriter, r *http.Request) {
	var companyID, expertID *int
	if v := r.URL.Query().Get("company_id"); v != "" {
		id, _ := strconv.Atoi(v)
		companyID = &id
	}
	if v := r.URL.Query().Get("expert_id"); v != "" {
		id, _ := strconv.Atoi(v)
		expertID = &id
	}
	list, err := h.repo.ListReports(r.Context(), companyID, expertID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) GetReport(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	rep, err := h.repo.GetReport(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, rep)
}

func (h *ExpertHandler) UpdateReportStatus(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var body struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateReportStatus(r.Context(), id, body.Status); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": body.Status})
}

func (h *ExpertHandler) ApproveReport(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.ApproveReport(r.Context(), id); err != nil {
		http.Error(w, `{"error":"approve failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "approved"})
}

func (h *ExpertHandler) DeleteReport(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteReport(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Panel Measurements ────────────────────────────────────

func (h *ExpertHandler) CreatePanelMeasurements(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertPanelMeasurement
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreatePanelMeasurements(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetPanelMeasurements(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetPanelMeasurements(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdatePanelMeasurements(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertPanelMeasurement
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdatePanelMeasurements(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Interior Checks ───────────────────────────────────────

func (h *ExpertHandler) CreateInteriorChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertInteriorCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateInteriorChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetInteriorChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetInteriorChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateInteriorChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertInteriorCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateInteriorChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Exterior Checks ───────────────────────────────────────

func (h *ExpertHandler) CreateExteriorChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertExteriorCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateExteriorChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetExteriorChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetExteriorChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateExteriorChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertExteriorCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateExteriorChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Mechanical Checks ─────────────────────────────────────

func (h *ExpertHandler) CreateMechanicalChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertMechanicalCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateMechanicalChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetMechanicalChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetMechanicalChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateMechanicalChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertMechanicalCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateMechanicalChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Electronic Checks ─────────────────────────────────────

func (h *ExpertHandler) CreateElectronicChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertElectronicCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateElectronicChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetElectronicChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetElectronicChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateElectronicChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertElectronicCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateElectronicChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Tire Checks ───────────────────────────────────────────

func (h *ExpertHandler) CreateTireChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertTireCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateTireChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetTireChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetTireChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateTireChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertTireCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateTireChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Tramer Record ─────────────────────────────────────────

func (h *ExpertHandler) CreateTramerRecord(w http.ResponseWriter, r *http.Request) {
	var tr domain.ExpertTramerRecord
	if err := json.NewDecoder(r.Body).Decode(&tr); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateTramerRecord(r.Context(), &tr); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, tr)
}

func (h *ExpertHandler) GetTramerRecord(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetTramerRecord(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateTramerRecord(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertTramerRecord
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateTramerRecord(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Test Drive ────────────────────────────────────────────

func (h *ExpertHandler) CreateTestDrive(w http.ResponseWriter, r *http.Request) {
	var td domain.ExpertTestDrive
	if err := json.NewDecoder(r.Body).Decode(&td); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateTestDrive(r.Context(), &td); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, td)
}

func (h *ExpertHandler) GetTestDrive(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	td, err := h.repo.GetTestDrive(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, td)
}

func (h *ExpertHandler) UpdateTestDrive(w http.ResponseWriter, r *http.Request) {
	var td domain.ExpertTestDrive
	if err := json.NewDecoder(r.Body).Decode(&td); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateTestDrive(r.Context(), &td); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, td)
}

// ── Dyno Test ─────────────────────────────────────────────

func (h *ExpertHandler) CreateDynoTests(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertDynoTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateDynoTests(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetDynoTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetDynoTests(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateDynoTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertDynoTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateDynoTests(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Photos ────────────────────────────────────────────────

func (h *ExpertHandler) CreatePhotos(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertPhoto
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreatePhotos(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) ListPhotos(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.ListPhotos(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ═══════════════════════════════════════════════════════════
// NEW TABLES (000014)
// ═══════════════════════════════════════════════════════════

// ── Emission Tests ────────────────────────────────────────

func (h *ExpertHandler) CreateEmissionTests(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertEmissionTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateEmissionTests(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetEmissionTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetEmissionTests(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateEmissionTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertEmissionTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateEmissionTests(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Fluid Tests ───────────────────────────────────────────

func (h *ExpertHandler) CreateFluidTests(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertFluidTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateFluidTests(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetFluidTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetFluidTests(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateFluidTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertFluidTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateFluidTests(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Handbrake Tests ───────────────────────────────────────

func (h *ExpertHandler) CreateHandbrakeTests(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertHandbrakeTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateHandbrakeTests(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetHandbrakeTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetHandbrakeTests(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateHandbrakeTests(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertHandbrakeTest
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateHandbrakeTests(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Four Wheel Drive Checks ───────────────────────────────

func (h *ExpertHandler) CreateFourWheelDriveChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertFourWheelDriveCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateFourWheelDriveChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetFourWheelDriveChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetFourWheelDriveChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateFourWheelDriveChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertFourWheelDriveCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateFourWheelDriveChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Belt Checks ───────────────────────────────────────────

func (h *ExpertHandler) CreateBeltChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertBeltCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateBeltChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetBeltChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetBeltChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateBeltChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertBeltCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateBeltChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Chassis Checks ────────────────────────────────────────

func (h *ExpertHandler) CreateChassisChecks(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertChassisCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateChassisChecks(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetChassisChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetChassisChecks(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateChassisChecks(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertChassisCheck
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateChassisChecks(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Extra Equipment ───────────────────────────────────────

func (h *ExpertHandler) CreateExtraEquipment(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertExtraEquipment
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateExtraEquipment(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetExtraEquipment(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetExtraEquipment(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateExtraEquipment(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertExtraEquipment
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateExtraEquipment(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Mandatory Equipment ───────────────────────────────────

func (h *ExpertHandler) CreateMandatoryEquipment(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertMandatoryEquipment
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateMandatoryEquipment(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetMandatoryEquipment(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetMandatoryEquipment(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateMandatoryEquipment(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertMandatoryEquipment
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateMandatoryEquipment(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Acceptance Criteria ───────────────────────────────────

func (h *ExpertHandler) CreateAcceptanceCriteria(w http.ResponseWriter, r *http.Request) {
	var items []*domain.ExpertAcceptanceCriteria
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateAcceptanceCriteria(r.Context(), items); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, items)
}

func (h *ExpertHandler) GetAcceptanceCriteria(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	list, err := h.repo.GetAcceptanceCriteria(r.Context(), reportID)
	if err != nil {
		http.Error(w, `{"error":"get failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ExpertHandler) UpdateAcceptanceCriteria(w http.ResponseWriter, r *http.Request) {
	reportID, _ := strconv.Atoi(chi.URLParam(r, "reportId"))
	var items []*domain.ExpertAcceptanceCriteria
	if err := json.NewDecoder(r.Body).Decode(&items); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateAcceptanceCriteria(r.Context(), reportID, items); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}
