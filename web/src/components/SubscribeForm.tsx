"use client";

import { FormEvent, useState } from "react";

type Phase = "idle" | "submitting" | "saved" | "duplicate";

export function SubscribeForm() {
  const [email, setEmail] = useState("");
  const [phase, setPhase] = useState<Phase>("idle");
  const [error, setError] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setPhase("submitting");

    try {
      const response = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const payload = (await response.json()) as {
        ok?: boolean;
        error?: string;
        alreadyJoined?: boolean;
      };

      if (!response.ok || !payload.ok) {
        setPhase("idle");
        setError(payload.error ?? "Something went wrong. Try again.");
        return;
      }

      setPhase(payload.alreadyJoined ? "duplicate" : "saved");
    } catch {
      setPhase("idle");
      setError("The signup page could not be reached. Try again.");
    }
  }

  if (phase === "saved" || phase === "duplicate") {
    return (
      <div className="status" role="status">
        <h2>{phase === "saved" ? "You're on the list." : "Already on the list."}</h2>
        <p className="status-copy">
          {phase === "saved"
            ? "This machine saved your address. A confirmation email starts once sending is connected. Nothing has been mailed yet."
            : "This address is already stored on this machine. Nothing has been mailed."}
        </p>
        <button
          className="text-button"
          type="button"
          onClick={() => {
            setEmail("");
            setPhase("idle");
          }}
        >
          Use a different address
        </button>
      </div>
    );
  }

  return (
    <form className="subscribe" onSubmit={onSubmit} noValidate>
      <label htmlFor="email">Email address</label>
      <div className="fields">
        <input
          id="email"
          name="email"
          type="email"
          inputMode="email"
          autoComplete="email"
          placeholder="you@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          disabled={phase === "submitting"}
        />
        <button type="submit" disabled={phase === "submitting"}>
          {phase === "submitting" ? "Saving…" : "Send me the letter"}
        </button>
      </div>
      {error ? (
        <p className="form-error" role="alert">
          {error}
        </p>
      ) : (
        <p className="fine-print">
          One letter each Sunday. You will confirm by email before the first
          issue arrives. Unsubscribe any time.
        </p>
      )}
    </form>
  );
}
