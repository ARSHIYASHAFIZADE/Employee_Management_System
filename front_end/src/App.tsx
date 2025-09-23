import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Employees from "./pages/Employees";
import Login from "./pages/Login";
import { AuthProvider } from "./context/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <nav className="bg-blue-600 text-white p-4 flex gap-6">
          <Link to="/">Dashboard</Link>
          <Link to="/employees">Employees</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </nav>

        <main className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
      </Router>
    </AuthProvider>
  );
}
