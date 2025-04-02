// These are generated dynamically through `make_static_app.py`
const prompt = `"!PROMPT"`;
const responseSchema = "!RESPONSE_SCHEMA";

document.addEventListener("DOMContentLoaded", function () {
  const analyzeBtn = document.getElementById("analyze-btn");
  const downloadBtn = document.getElementById("download-btn");
  const articleTextArea = document.getElementById("article-text");
  const apiKeyInput = document.getElementById("api-key");
  const outputContainer = document.getElementById("output-container");
  const outputJson = document.getElementById("output-json");
  const spinner = document.querySelector(".spinner-border");

  analyzeBtn.addEventListener("click", async function () {
    const articleText = articleTextArea.value.trim();
    const apiKey = apiKeyInput.value.trim();

    if (!articleText) {
      alert("Please enter article text");
      return;
    }

    if (!apiKey) {
      alert("Please enter your Google API Key");
      return;
    }

    // Show loading state
    analyzeBtn.disabled = true;
    spinner.style.display = "inline-block";
    outputContainer.style.display = "none";

    try {
      const generationConfig = {
        temperature: 0.0,
        responseMimeType: "application/json",
        response_schema: responseSchema,
      };

      // Step 2: Call Gemini API from the client side
      const response = await fetch(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" +
          apiKey,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt + "\n" + articleText }] }],
            generationConfig: generationConfig,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || "API request failed");
      }

      const data = await response.json();

      let metricsResult;
      if (data.candidates && data.candidates[0] && data.candidates[0].content) {
        const parts = data.candidates[0].content.parts;
        if (parts && parts.length > 0) {
          metricsResult = parts[0].text;

          if (
            typeof parts[0].functionResponse === "object" &&
            parts[0].functionResponse !== null
          ) {
            metricsResult = parts[0].functionResponse;
          } else if (typeof parts[0].text === "string") {
            try {
              metricsResult = JSON.parse(parts[0].text);
            } catch (e) {}
          }
        }
      }

      // Display the results
      outputJson.textContent = JSON.stringify(metricsResult, null, 2);
      outputContainer.style.display = "block";

      // Store the result for download
      window.metricsResult = metricsResult;
    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error.message);
    } finally {
      // Reset loading state
      analyzeBtn.disabled = false;
      spinner.style.display = "none";
    }
  });

  downloadBtn.addEventListener("click", function () {
    if (!window.metricsResult) {
      alert("No results to download");
      return;
    }

    const jsonString = JSON.stringify(window.metricsResult, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "metrics_results.json";
    document.body.appendChild(a);
    a.click();

    // Cleanup
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  });
});
