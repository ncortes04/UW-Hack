from classify import load_model, classify_skin_image

def main():
    test_image = r"C:\Users\troyr\Desktop\UW-Hack\dataset\test_set\FU-athlete-foot\FU-athlete-foot (1).jpeg"

    try:
        model = load_model()
        label, confidence = classify_skin_image(model, test_image)

        if label:
            print(f"\n🩺 Diagnosis Suggestion: {label}")
            print(f"🔬 Confidence: {confidence * 100:.2f}%")
        else:
            print("⚠️ Prediction failed.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
