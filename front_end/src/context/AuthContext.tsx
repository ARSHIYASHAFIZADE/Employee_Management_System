import { createContext, useContext, useEffect, useState } from "react";
import { loginUser, logoutUser, getCurrentUser, registerUser } from "../services/AuthService";
import type {ReactNode} from 'react'

interface AuthContextType {
  user: any;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => useContext(AuthContext)!;

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    (async () => {
      try {
        const me = await getCurrentUser();
        setUser(me);
      } catch {
        setUser(null);
      }
    })();
  }, []);

  const login = async (email: string, password: string) => {
    await loginUser(email, password);
    const me = await getCurrentUser();
    setUser(me);
  };

  const register = async (email: string, password: string) => {
    await registerUser(email, password);
  };

  const logout = () => {
    logoutUser();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
