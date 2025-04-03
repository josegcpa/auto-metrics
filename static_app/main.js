// These are generated dynamically through `make_static_app.py`
const prompt = `
# Instructions
You are an expert radiologist with decades of experience in developing and implementing clinical artificial intelligence.
You have to offer ratings to a scientific article of clinical importance at the end of this prompt according to a set of criteria.
You must answer carefully and thoughtfully, considering the context of the article and your expertise.
Be extremely thorough and conservative with your answers as these tools are supposed to be deployed in the clinic.

# Evaluation
## Metrics definition
There are 30 criteria in total and each criterion is grouped into one of 9 categories.
There are, additionally, 5 conditions which define whether some criterion should be filled or not.
The 5 Conditions are defined below under "## Conditions". A short explanation is provided for each.
The 30 criteria are defined below under "## Criteria". Each is grouped under its respective category. A short explanation is provided for each.

## Rating Rubric
No: no evidence that this criterion is being followed in this publication
Yes: evidence that this criterion is being followed in this publication
n/a: not applicable
Reason: a short explanation for each ranking

# Input format
The article text is provided below under "# Article text". Anything outside of this text should not be evaluated.

# Output format
You have to output:
- a summary of the article accurately representing the main conclusion of the article
- the answers for conditions (Yes, No) and a short explanation for your decision
- the ratings (Yes, No or n/a) for each criterion and a short explanation for your decision

## Conditions

* Condition 1: Does the study include segmentation? - "Segmentation" refers to i) Fine delineation of a region or volume of interest; ii) Rough delineation with bounding boxes; or, iii) cropping the image around a region of interest.
* Condition 2: Does the study include fully automated segmentation? - "Fully automated segmentation" refers to segmentation process without any human intervention.
* Condition 3: Does the study include hand-crafted feature extraction? - "Hand-crafted radiomic features" (i.e., traditional radiomic features) are created in advance by human experts or mathematicians.
* Condition 4: Does the study include tabular data? - "Tabular data" refers to data that is organized in a table with rows and columns (i.e., numeric radiomic features in a tabulated format, which  is usually seen in hand-crafted and some deep learning-based studies as deep features).
* Condition 5: Does the study include end-to-end deep learning? - "End-to-end deep learning" refers to the use of deep learning to directly process the image data and produce a classification or regression model.


## Criteria

### Study Design
* Item 1: Adherence to radiomics and/or machine learning-specific checklists or guidelines - Whether any guideline or checklist, e.g., CLEAR checklist, is used in designing and reporting, as appropriate for the study design (e.g., handcrafted radiomics or deep learning pipeline).
* Item 2: Eligibility criteria that describe a representative study population - Whether inclusion and exclusion criteria are explicitly defined. These should lead to a representative study sample that matches the general population of interest for the study aim.
* Item 3: High-quality reference standard with a clear definition - Whether the reference standard or outcome measure is representative of the current  clinical practice and robust. Examples of high-quality reference standards are preferably  histopathology, well-established clinical and genomic markers, the latest version of the prognostic  tools, guideline-based follow-up or consensus-based expert opinions. Examples of poor quality  reference standards are those based on qualitative image evaluation, images that are later  used for feature extraction, or outdated versions of prognostic tools.

### Imaging Data
* Item 4: Multi-center - Whether more than one institution is involved as a diagnostic imaging data source for radiomics analysis.
* Item 5: Clinical translatability of the imaging data source for radiomics analysis - Whether the source of the radiomics data is an imaging technique that reflects established standardization approaches, such as acquisition protocol guidelines (e.g., PI-RADS specifications).
* Item 6: Imaging protocol with acquisition parameters - Whether the image acquisition protocol is clearly reported to ensure the replicability of the method.
* Item 7: The interval between imaging used and reference standard - Whether the time interval between the diagnostic imaging exams (used as an input for the radiomics analysis) and the outcome measure/reference standard acquisition is appropriate to validate the presence or absence of target conditions of the radiomics analysis at the moment of the diagnostic imaging exams. If there is no mention of when the reference standard was acquired relative to the diagnostic imaging  exams, the answer should be "no".

### Segmentation
* Item 8: Transparent description of segmentation methodology - Whether the rules or the method of the segmentation are defined (e.g., margin shrinkage, peri-tumoral sampling, details of segmentation regardless of whether manual, semi-automated or automated methods are used). In the case of DL-based radiomics, the segmentation can refer to the rough delineation with bounding boxes or cropping the image around a region of interest. Answer only if Condition 1 are "yes".
* Item 9: Formal evaluation of fully automated segmentation - If a segmentation technique that does not require any sort of human intervention is used, examples of the results should be presented and a formal assessment of its accuracy compared to domain expert annotations included in the study (e.g., DICE score or Jaccard index compared with a radiologist's semantic annotation). Answer only if Condition 1 and 2 are "yes".
* Item 10: Test set segmentation masks produced by a single reader or automated tool - Whether final segmentation in the test set is produced by a single reader (manually or with a semi-automated tool) or an entirely automated tool, to better reflect clinical practice. Keep in mind that having a radiologist review the results of the automated segmentation is not considered clinical practice. Answer only if Condition 1 are "yes".

### Image Processing and Feature Extraction
* Item 11: Appropriate use of image preprocessing techniques with transparent description - Whether preprocessing of the images is appropriately performed  considering the imaging modality (e.g., gray level normalization for MRI, image registration in case of multiple contrasts or modalities) and feature extraction techniques (i.e., 2D or 3D) that are used. For instance, in the case of large slice thickness (e.g., u22655 mm), extreme upsampling (e.g., 1 x 1 x 1 mm3) of the volume might be inappropriate. In such a case, 2D feature extraction could be preferable, ensuring in-plane isotropy of the pixels. On the other hand, achieving isotropic voxel values should be targeted in 3D feature extraction, to allow for texture feature rotational invariance. Also, whether gray level discretization parameters (bin width, along with resulting gray level range, or bin count) are described in full detail. Description of different image types used (e.g., original, filtered) should also be included (e.g., high and low pass filter combinations for wavelet decomposition, sigma values for Laplacian of Gaussian edge enhancement filtering). If the image window is fixed, it should be clarified.
* Item 12: Use of standardized feature extraction software - Whether a standardized software (e.g., compliant with IBSI) was used for feature extraction, including information on the version number. Answer only if Condition 3 are "yes".
* Item 13: Transparent reporting of feature extraction parameters, otherwise providing a default configuration statement - Whether feature types (e.g., hand-crafted, deep features) and feature classes (for hand-crafted) are described. Also, if a default configuration statement is provided for the remaining feature extraction parameters. A file presenting the complete configuration of these settings should be included in the study materials (e.g., parameter file such as in YAML format, screenshot if a dedicated file for this is not available for the software). In the case of DL, neural network architecture along with all image operations should be described.

### Feature Processing
* Item 14: Removal of non-robust features - Whether unstable features are removed via test-retest, reproducibility analysis by analysis of different segmentations, or stability analysis [i.e., image perturbations]. Instability may be due to random noise introduced by manual or even automated image segmentation or exposed in a scan-rescan setting. The specific methods used should be clearly presented, with specific results for each component in multi-step feature removal pipelines. Answer only if Condition 4 are "yes".
* Item 15: Removal of redundant features - Whether dimensionality is reduced by selecting the more informative features such as with algorithm-based feature selection (e.g., LASSO coefficients, Random Forest feature importance), univariate correlation, collinearity, or variance analysis. The specific methods used should be clearly presented, with specific results for each component in multi-step feature removal pipelines. Answer only if Condition 4 are "yes".
* Item 16: Appropriateness of dimensionality compared to data size - Whether the number of instances and features in the final training data set is appropriate according to the research question and modeling algorithm. This should be demonstrated by statistical means, empirically through consistency of performance in validation and testing, or based on previous evidence in the literature. Answer only if Condition 4 are "yes".
* Item 17: Robustness assessment of end-to-end deep learning pipelines - Whether DL pipeline consistency of performance has been assessed in a test-retest setting, for example by a scan-rescan approach, use of segmentations by different readers, or stability analysis [i.e., image perturbations]. Answer only if Condition 5 are "yes".

### Preparation for Modeling
* Item 18: Proper data partitioning process - Whether the training-validation-test data split is done at the very beginning of the analysis pipeline, prior to any processing step. Data split should be random but reproducible (e.g., fixed random seed), preferably without altering outcome variable distribution in the test set (e.g., using a stratified data split). Moreover, the data split should be on the patient level, not the scan level (i.e., different scans of the same patient should be in the same set). Proper data partitioning should guarantee that all data processing (e.g., scaling, missing value imputation, oversampling or undersampling) is done blinded to the test set data. These techniques should be exclusively fitted on training (or development) data sets and then used to transform test data at the time of inference. If a single training-validation data split is not done and a resampling technique (e.g., cross-validation) is used instead, test data should always be handled separately from this.
* Item 19: Handling of confounding factors - Whether potential confounding factors were analyzed, identified if present, and removed if necessary (e.g., if it has a strong influence on generalizability). These may include different distributions of patient characteristics (e.g., gender, lesion stage or grade) across sites or scanners. Be sure to focus on  confounders stemming from the acquisition process, such as scanner type, manufacturer, or scanner parameters, or from the individual patient characteristics, such as age, weight, or comorbidities.

### Metrics and Comparison
* Item 20: Use of appropriate performance evaluation metrics for task - Whether appropriate accuracy metrics are reported, such as AUC for Receiver Operating Characteristics (ROC) or Precision-Recall (PRC) curves and confusion matrix-derived accuracy metrics (e.g., specificity, sensitivity, precision, F1 score) for classification tasks; MSE, RMSE, and MAE for regression tasks. For classification tasks, the confusion matrix should always be included, to allow the calculation of additional metrics. If training a DL network, loss curves should be presented.
* Item 21: Consideration of uncertainty - Whether uncertainty measures are included in the analysis, such as 95% confidence interval (CI), standard deviation (SD), or standard error (SE). Report on methodology to derive that distribution (ie. bootstrapping with replacement, etc).
* Item 22: Calibration assessment - Whether the final model's calibration is assessed.
* Item 23: Use of uni-parametric imaging or proof of its inferiority - Use of a single imaging set (such as a single MRI sequence rather than multiple, or a single phase in a dynamic contrast-enhanced scan) should be preferred, as multi-parametric imaging may unnecessarily increase data dimensionality and risk of overfitting. Therefore, in the case of multi-parametric studies, uni-parametric evaluations should also be performed to justify the need for a multi-parametric approach by formally comparing their performance (e.g., DeLong's or McNemar's tests). This item is also intended to reward studies that experimentally justify the use of more complex models compared to simpler alternatives, in regard to input data type. Uni-parametric imaging implies the acquisition of a single  imaging modality, as opposed to multi-parametric imaging, which involves the acquisition of multiple  imaging modalities.
* Item 24: Comparison with a non-radiomic approach or proof of added clinical value - Whether a non-radiomic method that is representative of the clinical practice is included in the analysis for comparison purposes. Non-radiomic methods might include semantic features,  RADS or RECIST scoring, and simple volume or size evaluations. If no non-radiomics method is available,  proof of improved diagnostic accuracy (e.g., improved performance of a radiologist assisted by the  model's output) or patient outcome (e.g., decision analysis, overall survival) should be provided.  In any case, the comparison should be done with an appropriate statistical method to evaluate the  added practical and clinical value of the model (e.g., DeLong's test for AUC comparison, decision  curve analysis for net benefit comparison, Net Reclassification Index). Furthermore, in case of  multiple comparisons, multiple testing correction methods (e.g., Bonferroni) should be considered  in order to reduce the false discovery rate provided that the statistical comparison is done with  a frequentist approach (rather than Bayesian).
* Item 25: Comparison with simple or classical statistical models - Whether a comparison with a simple baseline reference model (such as a Zero Rules/No Information Rate classifier) was performed. Use of machine learning methods should be justified by proof of increased performance. In any case, the comparison should be done with an appropriate statistical method (e.g., DeLong's test for AUC comparison, Net Reclassification Index). Furthermore, in case of multiple comparisons, multiple testing correction methods (e.g., Bonferroni, Benjamini-Hochberg, or Tukey) should be considered in order to reduce the false discovery rate provided that the statistical comparison is done with a frequentist approach (rather than Bayesian).

### Testing
* Item 26: Internal testing - Whether the model is tested on an independent data set that is sampled from the same source as the training and/or validation sets.
* Item 27: External testing - Whether the model is tested with independent data from other institution(s). This also applies to the studies validating the previously published models trained at another institution.

### Open Science
* Item 28: Data availability - Whether any imaging, segmentation, clinical, or radiomics analysis data is shared with the public.
* Item 29: Code availability - Whether all scripts related to automatic segmentation and/or modeling are shared with the public. These should include clear instructions for their implementation (e.g., accompanying documentation, tutorials).
* Item 30: Model availability - Whether the final model is shared in the form of a raw model file or as a ready-to-use system. If automated segmentation was employed, the corresponding trained model should also be made available to allow replication. These should include clear instructions for their usage (e.g., accompanying documentation, tutorials).


# Article text

`;
const responseSchema = {"properties": {"Summary": {"title": "Summary", "type": "string"}, "Item1": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item2": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item3": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item4": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item5": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item6": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item7": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Condition1": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Condition2": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item8": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item9": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item10": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Condition3": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item11": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item12": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item13": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Condition4": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Condition5": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item14": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item15": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item16": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item17": {"properties": {"rating": {"enum": ["yes", "no", "n/a"], "title": "RatingWithNAEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "RatingWithNA", "type": "object"}, "Item18": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item19": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item20": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item21": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item22": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item23": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item24": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item25": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item26": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item27": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item28": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item29": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}, "Item30": {"properties": {"rating": {"enum": ["yes", "no"], "title": "RatingEnum", "type": "string"}, "reason": {"title": "Reason", "type": "string"}}, "required": ["rating", "reason"], "title": "Rating", "type": "object"}}, "required": ["Summary", "Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7", "Condition1", "Condition2", "Item8", "Item9", "Item10", "Condition3", "Item11", "Item12", "Item13", "Condition4", "Condition5", "Item14", "Item15", "Item16", "Item17", "Item18", "Item19", "Item20", "Item21", "Item22", "Item23", "Item24", "Item25", "Item26", "Item27", "Item28", "Item29", "Item30"], "title": "Metrics", "type": "object"};

document.addEventListener("DOMContentLoaded", function () {
  const analyzeBtn = document.getElementById("analyze-btn");
  const downloadBtn = document.getElementById("download-btn");
  const articleTextArea = document.getElementById("article-text");
  const apiKeyInput = document.getElementById("api-key");
  const outputContainer = document.getElementById("output-container");
  const outputBody = document.getElementById("output-table-container");
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
      console.log("metricsResult", metricsResult);
      var key = "";
      var outputTable = `
        <tr>
          <td><b>Item</b></td><td><b>Rating</b></td><td><b>Reason</b></td>
        </tr>`;
      for (let idx in responseSchema.required) {
        key = responseSchema.required.at(idx);
        if (key === "Summary") {
          outputBody.innerHTML = `<h2>Summary</h2><p>${metricsResult[key]}</p>`;
        } else if (key.includes("Condition")) {
          outputTable += `
          <tr class="condition">
            <td>${key}</td><td>${metricsResult[key].rating}</td><td>${metricsResult[key].reason}</td>
          </tr>`;
        } else if (key.includes("Item")) {
          outputTable += `
          <tr class="item">
            <td>${key}</td><td>${metricsResult[key].rating}</td><td>${metricsResult[key].reason}</td>
          </tr>`;
        }
      }
      outputBody.innerHTML += `<table>${outputTable}</table>`;
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
