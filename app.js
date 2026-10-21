const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/jpg"];

const elements = {
  dropzone: document.querySelector("#dropzone"),
  fileInput: document.querySelector("#file-input"),
  chooseButton: document.querySelector("#choose-button"),
  uploadEmpty: document.querySelector("#upload-empty"),
  previewState: document.querySelector("#preview-state"),
  previewImage: document.querySelector("#preview-image"),
  removeButton: document.querySelector("#remove-button"),
  analyzeButton: document.querySelector("#analyze-button"),
  buttonLabel: document.querySelector(".button-label"),
  buttonLoading: document.querySelector(".button-loading"),
  fileError: document.querySelector("#file-error"),
  resultSection: document.querySelector("#result-section"),
  resultImage: document.querySelector("#result-image"),
  resultStatus: document.querySelector("#result-status"),
  resultStatusLabel: document.querySelector("#result-status-label"),
  resultStatusDot: document.querySelector(".result-status-dot"),
  resultTitle: document.querySelector("#result-title"),
  resultDescription: document.querySelector("#result-description"),
  confidenceValue: document.querySelector("#confidence-value"),
  confidenceBar: document.querySelector("#confidence-bar"),
  newAnalysisButton: document.querySelector("#new-analysis-button"),
};

let selectedFile = null;
let previewUrl = null;

function showError(message) {
  elements.fileError.textContent = message;
  elements.fileError.hidden = false;
}

function clearError() {
  elements.fileError.hidden = true;
  elements.fileError.textContent = "";
}

function setSelectedFile(file) {
  clearError();
  if (!file) return;
  if (!ACCEPTED_TYPES.includes(file.type)) {
    showError("Định dạng chưa được hỗ trợ. Hãy chọn ảnh JPG, JPEG hoặc PNG.");
    return;
  }
  if (file.size > MAX_FILE_SIZE) {
    showError("Ảnh quá lớn. Vui lòng chọn ảnh có dung lượng tối đa 10 MB.");
    return;
  }

  selectedFile = file;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);
  elements.previewImage.src = previewUrl;
  elements.uploadEmpty.hidden = true;
  elements.previewState.hidden = false;
  elements.analyzeButton.disabled = false;
  elements.resultSection.hidden = true;
}

function resetUpload() {
  selectedFile = null;
  elements.fileInput.value = "";
  elements.uploadEmpty.hidden = false;
  elements.previewState.hidden = true;
  elements.analyzeButton.disabled = true;
  clearError();
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
    previewUrl = null;
  }
}

function setLoading(isLoading) {
  elements.analyzeButton.disabled = isLoading;
  elements.buttonLabel.hidden = isLoading;
  elements.buttonLoading.hidden = !isLoading;
  elements.buttonLoading.style.display = isLoading ? "flex" : "";
}

function showResult(prediction) {
  const confidence = Math.round(prediction.confidence * 100);
  const isFlooding = prediction.label === "flooding";
  elements.resultImage.src = previewUrl;
  elements.resultStatusLabel.textContent = isFlooding ? "Có dấu hiệu ngập" : "Chưa thấy dấu hiệu ngập";
  elements.resultStatus.style.color = isFlooding ? "var(--amber)" : "var(--green)";
  elements.resultStatusDot.style.background = isFlooding ? "var(--amber)" : "var(--green)";
  elements.resultTitle.textContent = isFlooding
    ? "Có dấu hiệu ngập trong ảnh"
    : "Chưa phát hiện dấu hiệu ngập rõ ràng";
  elements.resultDescription.textContent = isFlooding
    ? "Mô hình nhận thấy các đặc điểm hình ảnh phù hợp với nhóm Flooding."
    : "Mô hình nhận thấy các đặc điểm hình ảnh phù hợp với nhóm No Flooding.";
  elements.confidenceValue.textContent = `${confidence}%`;
  elements.confidenceBar.style.transform = `scaleX(${confidence / 100})`;
  elements.resultSection.hidden = false;
  elements.resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

elements.chooseButton.addEventListener("click", () => elements.fileInput.click());
elements.dropzone.addEventListener("click", (event) => {
  if (!event.target.closest("button")) elements.fileInput.click();
});
elements.dropzone.addEventListener("keydown", (event) => {
  if ((event.key === "Enter" || event.key === " ") && event.target === elements.dropzone) {
    event.preventDefault();
    elements.fileInput.click();
  }
});
elements.fileInput.addEventListener("change", (event) => setSelectedFile(event.target.files[0]));
elements.removeButton.addEventListener("click", (event) => {
  event.stopPropagation();
  resetUpload();
});
["dragenter", "dragover"].forEach((eventName) => {
  elements.dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropzone.classList.add("dragging");
  });
});
["dragleave", "drop"].forEach((eventName) => {
  elements.dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropzone.classList.remove("dragging");
  });
});
elements.dropzone.addEventListener("drop", (event) => setSelectedFile(event.dataTransfer.files[0]));
elements.analyzeButton.addEventListener("click", () => {
  if (!selectedFile) return;
  setLoading(true);
  clearError();
  const formData = new FormData();
  formData.append("image", selectedFile);
  fetch("/api/predict", { method: "POST", body: formData })
    .then(async (response) => {
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.error || "Không thể phân tích ảnh.");
      return payload;
    })
    .then((prediction) => {
    setLoading(false);
      showResult(prediction);
    })
    .catch((error) => {
      setLoading(false);
      showError(`${error.message} Hãy kiểm tra server model đã được khởi động chưa.`);
    });
});
elements.newAnalysisButton.addEventListener("click", () => {
  resetUpload();
  document.querySelector("#checker").scrollIntoView({ behavior: "smooth" });
});
