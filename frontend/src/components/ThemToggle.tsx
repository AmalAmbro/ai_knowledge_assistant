import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const stored = localStorage.getItem("theme") as "light" | "dark" | null;

    if (stored) {
      setTheme(stored);
      document.documentElement.setAttribute("data-theme", stored);
    } else {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const systemTheme = prefersDark ? "dark" : "light";
      setTheme(systemTheme);
      document.documentElement.setAttribute("data-theme", systemTheme);
    }
  }, []);

  const toggleTheme = () => {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  };

  return (
    <button onClick={toggleTheme} style={toggleStyle}>
      {theme === "light" ? "🌙 Dark mode" : "☀️ Light mode"}
    </button>
  );
}

const toggleStyle: React.CSSProperties = {
  position: "absolute",
  top: "24px",
  right: "24px",
  background: "transparent",
  border: "1px solid var(--border)",
  color: "var(--text-primary)",
  padding: "8px 14px",
  borderRadius: "10px",
  cursor: "pointer",
  fontSize: "0.85rem",
};
