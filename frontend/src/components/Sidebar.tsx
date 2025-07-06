import React from "react";
import { Link } from "react-router-dom";

const Sidebar: React.FC = () => (
  <aside className="w-64 bg-gray-100 h-screen p-4 border-r hidden md:block">
    <nav>
      <ul className="space-y-2">
        <li>
          <Link to="/" className="block py-2 px-4 rounded hover:bg-blue-100">Dashboard</Link>
        </li>
        
      </ul>
    </nav>
  </aside>
);

export default Sidebar;
