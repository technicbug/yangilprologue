document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("mol-form").addEventListener("submit", function (e) {
      e.preventDefault();
      calculate();
    });
  });
  
  function calculate() {
    const concentrationType = document.getElementById("concentrationType").value;
    const volumeUnit = document.getElementById("volumeUnit").value;
    let volume = parseFloat(document.getElementById("volume").value);
    if (volumeUnit === "mL") volume /= 1000;
    if (isNaN(volume) || volume <= 0) return showError("용액 부피를 정확히 입력하세요.");
  
    if (concentrationType === "percent") {
      const percent = parseFloat(document.getElementById("targetConcentration").value);
      const density = parseFloat(document.getElementById("soluteDensity").value);
      if (isNaN(percent) || isNaN(density) || percent <= 0 || density <= 0) {
        return showError("퍼센트 농도와 용액 밀도를 정확히 입력하세요.");
      }
      const solutionMass = volume * 1000 * density;
      const soluteMass = (percent / 100) * solutionMass;
      return showResult(`${soluteMass.toFixed(3)} g의 용질이 필요합니다.`);
    }
  
    const concentration = parseFloat(document.getElementById("targetConcentration").value);
    if (isNaN(concentration) || concentration <= 0) {
      return showError("몰농도를 정확히 입력하세요.");
    }
  
    const moles = concentration * volume;
    const soluteType = document.getElementById("soluteType").value;
  
    if (soluteType === "solid") {
      const molarMass = parseFloat(document.getElementById("molarMass").value);
      if (isNaN(molarMass) || molarMass <= 0) return showError("몰질량을 올바르게 입력하세요.");
      const mass = moles * molarMass;
      return showResult(`${mass.toFixed(3)} g의 고체 용질이 필요합니다.`);
    }
  
    const liquidMode = document.getElementById("liquidMode").value;
  
    if (liquidMode === "mass") {
      const molarMass = parseFloat(document.getElementById("molarMass").value);
      const density = parseFloat(document.getElementById("soluteDensity").value);
      if (isNaN(molarMass) || isNaN(density) || molarMass <= 0 || density <= 0) {
        return showError("몰질량과 밀도를 올바르게 입력하세요.");
      }
      const mass = moles * molarMass;
      const vol_mL = mass / density;
      return showResult(`${mass.toFixed(3)} g (${vol_mL.toFixed(2)} mL)의 액체 용질이 필요합니다.`);
    }
  
    if (liquidMode === "stock") {
      const stockType = document.getElementById("stockConcentrationType").value;
  
      if (stockType === "mol") {
        const stockConc = parseFloat(document.getElementById("stockConcentration").value);
        const density = parseFloat(document.getElementById("stockDensity").value);
        if (isNaN(stockConc) || isNaN(density) || stockConc <= 0 || density <= 0) {
          return showError("원액의 농도와 밀도를 올바르게 입력하세요.");
        }
        const requiredVolume = (concentration * volume) / stockConc;
        const mass = requiredVolume * density;
        return showResult(`${mass.toFixed(3)} g (${(requiredVolume * 1000).toFixed(2)} mL)의 액체 원액이 필요합니다.`);
      }
  
      if (stockType === "percent") {
        const stockPercent = parseFloat(document.getElementById("stockConcentration").value);
        const density = parseFloat(document.getElementById("stockDensity").value);
  
        if (
          isNaN(concentration) || isNaN(stockPercent) || isNaN(density) ||
          concentration <= 0 || stockPercent <= 0 || density <= 0
        ) {
          return showError("목표 퍼센트, 원액 퍼센트, 밀도를 정확히 입력하세요.");
        }
  
        const solutionMass = volume * 1000 * density;
        const requiredSoluteMass = (concentration / 100) * solutionMass;
        const requiredStockMass = (requiredSoluteMass * 100) / stockPercent;
        const requiredVolume = requiredStockMass / density;
  
        return showResult(`${requiredStockMass.toFixed(3)} g (${requiredVolume.toFixed(2)} mL)의 액체 원액이 필요합니다.`);
      }
    }
  }
  
  function showResult(msg) {
    const resultBox = document.getElementById("result");
    const resultText = document.getElementById("calculated-amount");
    resultText.textContent = msg;
    resultBox.style.display = "block";
  }
  
  function showError(msg) {
    showResult(msg);
  }
  