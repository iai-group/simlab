import React, { useEffect, useState } from "react";

export type User = {
  username: string;
};

export type AuthContextType = {
  user: User | null;
  setUser: (user: User | null) => void;
};

type AuthProviderProps = {
  children: React.ReactNode;
};

export const AuthContext = React.createContext<AuthContextType>({
  user: null,
  setUser: () => {},
});

export const AuthProvider: React.FC<AuthProviderProps> = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [user, setUser] = useState<User | null>(() => {
    const storedUser = sessionStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });

  useEffect(() => {
    sessionStorage.setItem("user", JSON.stringify(user));
  }, [user]);

  const handleSetUser = (newUser: User | null) => {
    setUser(newUser);
  };

  return (
    <AuthContext.Provider value={{ user, setUser: handleSetUser }}>
      {children}
    </AuthContext.Provider>
  );
};
