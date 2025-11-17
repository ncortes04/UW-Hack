import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SkinWizard.css";
const SkinWizard = () => {
  const navigate = useNavigate();

  const steps = [
    {
      question: "What type of skin do you have?",
      options: ["Oily", "Dry", "Combination", "Sensitive", "Not sure"],
      key: "skinType",
    },
    {
      question: "Where is the issue located?",
      options: ["Face", "Scalp", "Hands", "Feet", "Torso", "Other"],
      key: "location",
    },
    {
      question: "How long has the issue been present?",
      options: [
        "Less than a week",
        "1–2 weeks",
        "Over a month",
        "Several months",
      ],
      key: "duration",
    },
    {
      question: "Upload an image of the affected area",
      isFileUpload: true,
      key: "image",
    },
  ];

  const [stepIndex, setStepIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [imagePreview, setImagePreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleOptionClick = (value) => {
    const currentKey = steps[stepIndex].key;
    setAnswers((prev) => ({ ...prev, [currentKey]: value }));
    setStepIndex((prev) => prev + 1);
  };

  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setAnswers((prev) => ({ ...prev, image: file }));
    setImagePreview(URL.createObjectURL(file));
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("image", file);
      formData.append("skinType", answers.skinType || "");
      formData.append("location", answers.location || "");
      formData.append("duration", answers.duration || "");

      const res = await fetch("http://localhost:5000/api/classify-image", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.label) {
        setPrediction(data.label);
        setStepIndex((prev) => prev + 1);
      } else {
        alert("Could not classify image.");
      }
    } catch (err) {
      alert("Image upload failed.");
      console.error(err);
    }

    setLoading(false);
  };

  const handleChatRedirect = () => {
    navigate("/home");
  };

  return (
    <div className="wizard-container">
      <div className="wizard-box">
        {stepIndex < steps.length ? (
          <>
            <h2 className="wizard-question">{steps[stepIndex].question}</h2>

            {steps[stepIndex].isFileUpload ? (
              <>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="wizard-upload"
                />
                {imagePreview && (
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="wizard-preview"
                  />
                )}
                {loading && <p>⏳ Classifying image...</p>}
              </>
            ) : (
              <ul className="wizard-options">
                {steps[stepIndex].options.map((opt, i) => (
                  <li
                    key={i}
                    className="wizard-option"
                    onClick={() => handleOptionClick(opt)}
                  >
                    {opt}
                  </li>
                ))}
              </ul>
            )}
          </>
        ) : prediction ? (
          <>
            <h2 className="wizard-complete">🤖 Possible Diagnosis:</h2>
            <p style={{ fontSize: "1.25rem", marginBottom: "1rem" }}>
              <strong>{prediction}</strong>
            </p>
            <p>
              Would you like to chat with our AI assistant for personalized
              advice?
            </p>
            <div style={{ marginTop: "1rem" }}>
              <button className="wizard-button" onClick={handleChatRedirect}>
                Yes, continue to chat 💬
              </button>
              <button
                className="wizard-button-outline"
                onClick={() => alert("You can come back anytime!")}
              >
                No thanks
              </button>
            </div>
          </>
        ) : (
          <h2>⚠️ Something went wrong. Please try again.</h2>
        )}
      </div>
    </div>
  );
};

export default SkinWizard;
