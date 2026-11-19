
// ==========================================
// CODEGUARD AI - FRONTEND LOGIC
// ==========================================

const codeInput = document.getElementById("codeInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultStatus = document.getElementById("resultStatus");

// Score elements
const qualityScore = document.getElementById("qualityScore");
const qualityLevel = document.getElementById("qualityLevel");

const bugRisk = document.getElementById("bugRisk");
const riskLevel = document.getElementById("riskLevel");

// Metrics
const metricLines = document.getElementById("metricLines");
const metricFunctions = document.getElementById("metricFunctions");
const metricBranches = document.getElementById("metricBranches");
const metricLoops = document.getElementById("metricLoops");
const metricComplexity = document.getElementById("metricComplexity");
const metricNesting = document.getElementById("metricNesting");

// Analysis message
const analysisMessage = document.getElementById("analysisMessage");

// Findings and recommendations
const findingsContainer = document.getElementById("findingsContainer");
const recommendationsContainer = document.getElementById("recommendationsContainer");
// ==========================================
// CODEMIRROR PYTHON EDITOR
// ==========================================

// ==========================================
// CODEMIRROR PYTHON EDITOR
// ==========================================

let codeEditor = null;

function initializeCodeEditor() {

    if (codeEditor) {
        codeEditor.refresh();
        return;
    }

    codeEditor = CodeMirror.fromTextArea(codeInput, {
        mode: "python",
        theme: "dracula",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        viewportMargin: 20
    });

    codeEditor.setSize("100%", 380);
}
// PAGE NAVIGATION
const heroSection = document.querySelector(".hero");
const editorScreen = document.getElementById("editorScreen");
const openAnalyzerBtn = document.getElementById("openAnalyzerBtn");
const backToHomeBtn = document.getElementById("backToHomeBtn");

openAnalyzerBtn.addEventListener("click", () => {

    heroSection.classList.add("hidden");
    editorScreen.classList.add("active");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    setTimeout(() => {
        if (codeEditor) {
            codeEditor.refresh();
        }
    }, 100);

});

backToHomeBtn.addEventListener("click", () => {
    editorScreen.classList.remove("active");
    heroSection.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
});


// ==========================================
// ANALYZE CODE
// ==========================================

analyzeBtn.addEventListener("click", async () => {
    console.log("ANALYZE BUTTON CLICKED");

    const code = codeInput.value.trim();
    console.log("Code sent for analysis:", code);

    if (!code) {
        showError("Please enter some Python code first.");
        return;
    }

    setLoading(true);

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Analysis failed.");
        }

        displayResults(data);

    } catch (error) {

        console.error("Analysis Error:", error);

        showError(
            error.message ||
            "Something went wrong while analyzing the code."
        );

    } finally {
        setLoading(false);
    }

});


// ==========================================
// DISPLAY RESULTS
// ==========================================

function displayResults(data) {

    // Quality score
    const quality = Number(data.quality_score ?? 0);

    qualityScore.textContent = quality.toFixed(1);

    qualityLevel.textContent =
        data.quality_level || getQualityLevel(quality);


    // Bug risk score
    const risk = Number(data.bug_risk ?? 0);

    bugRisk.textContent = risk.toFixed(1);

    riskLevel.textContent =
        data.risk_level || getRiskLevel(risk);


    // Code metrics
    const features = data.features || {};

    metricLines.textContent = features.lines ?? 0;
    metricFunctions.textContent = features.functions ?? 0;
    metricBranches.textContent = features.branches ?? 0;
    metricLoops.textContent = features.loops ?? 0;
    metricComplexity.textContent = features.complexity ?? 0;
    metricNesting.textContent = features.nesting_depth ?? 0;


    // Overall analysis message
    analysisMessage.textContent =
        generateAnalysisMessage(quality, risk);


    // Findings
    displayFindings(data.findings || []);


    // Recommendations
    displayRecommendations(data.recommendations || []);


    // Success status
    resultStatus.textContent =
        "Analysis completed successfully";

    resultStatus.classList.remove("error");
    resultStatus.classList.add("success");


    // Scroll to results
    const resultSection =
        document.querySelector(".results-section");

    if (resultSection) {
        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

}


// ==========================================
// DISPLAY FINDINGS
// ==========================================

function displayFindings(findings) {

    findingsContainer.innerHTML = "";

    if (findings.length === 0) {

        findingsContainer.textContent =
            "No major issues were found in your code.";

        findingsContainer.className =
            "insight-list";

        return;
    }

    findings.forEach(finding => {

        const item = document.createElement("div");
        item.className = `finding-item ${finding.type || ""}`;

        const title = document.createElement("div");
        title.className = "finding-title";
        title.textContent = finding.title || "Code Finding";

        const message = document.createElement("div");
        message.className = "finding-message";
        message.textContent = finding.message || "";

        item.appendChild(title);
        item.appendChild(message);

        findingsContainer.appendChild(item);

    });

}


// ==========================================
// DISPLAY RECOMMENDATIONS
// ==========================================

function displayRecommendations(recommendations) {

    recommendationsContainer.innerHTML = "";

    if (recommendations.length === 0) {

        recommendationsContainer.textContent =
            "No additional suggestions available.";

        return;
    }

    recommendations.forEach(recommendation => {

        const item = document.createElement("div");
        item.className = "recommendation-item";

        const bullet = document.createElement("span");
        bullet.className = "recommendation-bullet";
        bullet.textContent = "✓";

        const text = document.createElement("span");
        text.textContent = recommendation;

        item.appendChild(bullet);
        item.appendChild(text);

        recommendationsContainer.appendChild(item);

    });

}


// ==========================================
// QUALITY LEVEL
// ==========================================

function getQualityLevel(score) {

    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    if (score >= 40) return "Needs Improvement";

    return "Poor";

}


// ==========================================
// BUG RISK LEVEL
// ==========================================

function getRiskLevel(score) {

    if (score <= 20) return "Low Risk";
    if (score <= 50) return "Moderate Risk";
    if (score <= 75) return "High Risk";

    return "Critical Risk";

}


// ==========================================
// OVERALL ANALYSIS MESSAGE
// ==========================================

function generateAnalysisMessage(quality, risk) {

    if (quality >= 80 && risk <= 20) {

        return "Your code is well organised and has a low predicted risk of errors. Keep following good coding practices.";

    }

    if (quality >= 60 && risk <= 50) {

        return "Your code has a good structure, but a few improvements may make it easier to understand and maintain.";

    }

    if (quality < 60 && risk > 50) {

        return "Your code may need some improvements. Try simplifying complex sections, avoiding repeated code and checking the highlighted issues.";

    }

    if (risk > 75) {

        return "Your code has a high predicted risk. Carefully review the highlighted areas and follow the suggested improvements.";

    }

    return "Your code can be improved further. Review the findings and recommendations to make it cleaner and easier to maintain.";

}


// ==========================================
// LOADING STATE
// ==========================================

function setLoading(isLoading) {

    analyzeBtn.disabled = isLoading;

    const buttonText =
        analyzeBtn.querySelector("span");

    if (buttonText) {
        buttonText.textContent =
            isLoading ? "Analyzing..." : "Analyze Code";
    }

    if (isLoading) {

        resultStatus.textContent =
            "Analyzing your code...";

        resultStatus.classList.remove("error", "success");

    }

}


// ==========================================
// ERROR MESSAGE
// ==========================================

function showError(message) {

    resultStatus.textContent = message;

    resultStatus.classList.remove("success");
    resultStatus.classList.add("error");

    analysisMessage.textContent = message;

}
