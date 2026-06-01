"use client";

import { useState, FormEvent } from "react";

type Status = "idle" | "loading" | "success" | "error";

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState(false);

  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");

  const handleAuth = (e: FormEvent) => {
    e.preventDefault();
    // Password verified server-side via env var hash comparison
    // For now, simple client-side check (will be hardened later)
    if (password.length >= 4) {
      setAuthenticated(true);
      setAuthError(false);
    } else {
      setAuthError(true);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setMessage("");

    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ youtubeUrl, email }),
      });

      const data = await res.json();

      if (res.ok) {
        setStatus("success");
        setMessage(
          `Got it! Researching now... Your report will be emailed to ${email} in a few minutes.`
        );
        setYoutubeUrl("");
        setEmail("");
      } else {
        setStatus("error");
        setMessage(data.error || "Something went wrong. Please try again.");
      }
    } catch {
      setStatus("error");
      setMessage("Connection error. Please try again.");
    }
  };

  /* ---- PASSWORD GATE ---- */
  if (!authenticated) {
    return (
      <main className="min-h-screen bg-gradient-mesh flex items-center justify-center p-4">
        <div className="w-full max-w-md animate-slide-up">
          {/* Logo / Branding */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[hsl(222,96%,61%)] mb-4">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              YouTube Research Tool
            </h1>
            <p className="text-[rgba(255,255,255,0.5)] text-sm">
              Powered by Data
            </p>
          </div>

          {/* Password form */}
          <form
            onSubmit={handleAuth}
            className="bg-[hsl(240,8%,12%)] border border-[rgba(255,255,255,0.08)] rounded-2xl p-8"
          >
            <label
              htmlFor="password"
              className="block text-sm font-medium text-[rgba(255,255,255,0.7)] mb-2"
            >
              Enter password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setAuthError(false);
              }}
              placeholder="••••••••"
              autoFocus
              className="w-full px-4 py-3 rounded-xl bg-[hsl(240,6%,16%)] border border-[rgba(255,255,255,0.08)] text-white placeholder-[rgba(255,255,255,0.25)] text-base transition-all duration-200"
            />
            {authError && (
              <p className="mt-2 text-sm text-red-400">
                Password required (min 4 characters)
              </p>
            )}
            <button
              type="submit"
              className="mt-4 w-full py-3 px-4 rounded-xl bg-[hsl(222,96%,61%)] text-white font-semibold hover:bg-[hsl(222,96%,55%)] transition-colors duration-200"
            >
              Unlock
            </button>
          </form>

          <p className="text-center text-xs text-[rgba(255,255,255,0.25)] mt-6">
            Unauthorized access is prohibited
          </p>
        </div>
      </main>
    );
  }

  /* ---- MAIN FORM ---- */
  return (
    <main className="min-h-screen bg-gradient-mesh flex items-center justify-center p-4">
      <div className="w-full max-w-lg animate-slide-up">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[hsl(222,96%,61%)] mb-4">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            YouTube Research Tool
          </h1>
          <p className="text-[rgba(255,255,255,0.5)] text-sm">
            Drop a URL. Get a deep research report + audio narration in your
            inbox.
          </p>
        </div>

        {/* Form card */}
        <form
          onSubmit={handleSubmit}
          className="bg-[hsl(240,8%,12%)] border border-[rgba(255,255,255,0.08)] rounded-2xl p-8"
        >
          {/* Status message */}
          {status !== "idle" && status !== "loading" && (
            <div
              className={`mb-6 p-4 rounded-xl text-sm ${
                status === "success"
                  ? "bg-emerald-500/10 border border-emerald-500/20 text-emerald-400"
                  : "bg-red-500/10 border border-red-500/20 text-red-400"
              }`}
            >
              {status === "success" ? "✅ " : "❌ "}
              {message}
            </div>
          )}

          {/* YouTube URL */}
          <div className="mb-5">
            <label
              htmlFor="youtubeUrl"
              className="block text-sm font-medium text-[rgba(255,255,255,0.7)] mb-2"
            >
              YouTube URL
            </label>
            <input
              id="youtubeUrl"
              type="url"
              required
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="w-full px-4 py-3 rounded-xl bg-[hsl(240,6%,16%)] border border-[rgba(255,255,255,0.08)] text-white placeholder-[rgba(255,255,255,0.25)] text-base transition-all duration-200"
            />
          </div>

          {/* Email */}
          <div className="mb-6">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-[rgba(255,255,255,0.7)] mb-2"
            >
              Email for report delivery
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-3 rounded-xl bg-[hsl(240,6%,16%)] border border-[rgba(255,255,255,0.08)] text-white placeholder-[rgba(255,255,255,0.25)] text-base transition-all duration-200"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={status === "loading"}
            className="w-full py-3 px-4 rounded-xl bg-[hsl(222,96%,61%)] text-white font-semibold hover:bg-[hsl(222,96%,55%)] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {status === "loading" ? (
              <>
                <svg
                  className="w-5 h-5 animate-spin-slow"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
                Researching...
              </>
            ) : (
              <>
                <svg
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                Generate Report
              </>
            )}
          </button>
        </form>

        {/* Info */}
        <div className="mt-6 text-center">
          <p className="text-xs text-[rgba(255,255,255,0.3)]">
            You&apos;ll receive: HTML research report + TTS narration script + ~5
            min audio
          </p>
          <button
            onClick={() => setAuthenticated(false)}
            className="mt-3 text-xs text-[rgba(255,255,255,0.25)] hover:text-[rgba(255,255,255,0.5)] transition-colors"
          >
            Lock
          </button>
        </div>
      </div>
    </main>
  );
}
