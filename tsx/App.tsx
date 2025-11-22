import { useState } from 'react';
import { LoginScreen } from './components/LoginScreen';
import { CustomerDashboard } from './components/CustomerDashboard';
import { StaffDashboard } from './components/StaffDashboard';
import { ManagerDashboard } from './components/ManagerDashboard';

export type UserRole = 'customer' | 'staff' | 'manager' | null;

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  const handleLogin = (user: User) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  if (!currentUser) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {currentUser.role === 'customer' && (
        <CustomerDashboard user={currentUser} onLogout={handleLogout} />
      )}
      {currentUser.role === 'staff' && (
        <StaffDashboard user={currentUser} onLogout={handleLogout} />
      )}
      {currentUser.role === 'manager' && (
        <ManagerDashboard user={currentUser} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;
