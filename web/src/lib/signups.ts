import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";

export type LocalSignup = {
  email: string;
  status: "pending";
  createdAt: string;
};

const filePath = path.join(process.cwd(), ".data", "signups.json");

async function readSignups(): Promise<LocalSignup[]> {
  try {
    const raw = await readFile(filePath, "utf8");
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed.filter(
      (row): row is LocalSignup =>
        typeof row === "object" &&
        row !== null &&
        typeof (row as LocalSignup).email === "string",
    );
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") {
      return [];
    }
    throw error;
  }
}

export async function saveLocalSignup(
  email: string,
): Promise<{ alreadyJoined: boolean }> {
  const signups = await readSignups();
  if (signups.some((row) => row.email === email)) {
    return { alreadyJoined: true };
  }

  signups.push({
    email,
    status: "pending",
    createdAt: new Date().toISOString(),
  });

  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, JSON.stringify(signups, null, 2));
  return { alreadyJoined: false };
}
