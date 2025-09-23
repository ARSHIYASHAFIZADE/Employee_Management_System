import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="bg-white p-6 shadow rounded">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      {user ? (
        <>
          <p>Welcome, <strong>{user.email}</strong></p>
          <button
            onClick={logout}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded"
          >
            Logout
          </button>
        </>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
}
