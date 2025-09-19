const COOKIE_NAME = "naomi_conversation_id";

const generateConversationId = () => {
  if (
    typeof crypto !== "undefined" &&
    typeof crypto.randomUUID === "function"
  ) {
    return crypto.randomUUID();
  }
  const rand = Math.random().toString(16).slice(2, 10);
  return `conv_${Date.now()}_${rand}`;
};

const readCookie = (name) => {
  if (typeof document === "undefined" || !document.cookie) return null;
  const cookie = document.cookie
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith(`${name}=`));
  if (!cookie) return null;
  const value = cookie.split("=")[1];
  return value ? decodeURIComponent(value) : null;
};

export const getConversationIdFromCookie = () => readCookie(COOKIE_NAME);

export const setConversationIdCookie = (id) => {
  if (typeof document === "undefined") return;
  const encoded = encodeURIComponent(id);
  document.cookie = `${COOKIE_NAME}=${encoded};path=/;SameSite=Lax`;
};

export const ensureConversationId = () => {
  const existing = getConversationIdFromCookie();
  if (existing) return existing;
  const id = generateConversationId();
  setConversationIdCookie(id);
  return id;
};

export const clearConversationIdCookie = () => {
  if (typeof document === "undefined") return;
  document.cookie = `${COOKIE_NAME}=;path=/;expires=Thu, 01 Jan 1970 00:00:00 GMT;SameSite=Lax`;
};
