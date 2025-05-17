import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SkinWizard from "./pages/SkinWizard";
import Home from "./pages/home";
function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Landing page */}
          <Route path="/" element={<SkinWizard />} />

          {/* GPT chat page */}
          <Route path="/home" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
