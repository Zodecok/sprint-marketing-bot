export function runtimeApiBase(): string | null {
  try {
    const url = new URL(window.location.href);
    return url.searchParams.get("api");
  } catch {
    return null;
  }
}

