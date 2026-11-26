import { normalizeEmail } from "@/lib/email";
import { saveLocalSignup } from "@/lib/signups";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json(
      { ok: false, error: "Enter a valid email address." },
      { status: 400 },
    );
  }

  const email = normalizeEmail(
    typeof body === "object" && body !== null && "email" in body
      ? (body as { email: unknown }).email
      : null,
  );

  if (!email) {
    return Response.json(
      { ok: false, error: "Enter a valid email address." },
      { status: 400 },
    );
  }

  if (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY) {
    return Response.json(
      {
        ok: false,
        error: "The hosted list is configured, and saving to it is not built yet.",
      },
      { status: 501 },
    );
  }

  try {
    const result = await saveLocalSignup(email);
    return Response.json({ ok: true, storage: "local", ...result });
  } catch {
    return Response.json(
      { ok: false, error: "The address could not be saved. Try again." },
      { status: 500 },
    );
  }
}
