const root = document.body;
const themeButtons = Array.from(document.querySelectorAll(".theme-btn"));
const savedTheme = localStorage.getItem("nails_inspo_theme") || "dark";

function applyTheme(theme) {
  root.setAttribute("data-theme", theme);
  themeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.themeValue === theme);
  });
  localStorage.setItem("nails_inspo_theme", theme);
}

themeButtons.forEach((button) => {
  button.addEventListener("click", () => applyTheme(button.dataset.themeValue));
});

applyTheme(savedTheme);

document.addEventListener("click", async (event) => {
  const button = event.target.closest(".remove-pin");
  if (!button) return;

  const telegramId = button.dataset.telegramId;
  const designId = button.dataset.designId;
  const card = button.closest(".pin-card");

  button.disabled = true;
  try {
    const response = await fetch(`/api/remove/${telegramId}/${designId}`, { method: "POST" });
    const payload = await response.json();
    if (payload.removed) {
      card.remove();
    } else {
      button.disabled = false;
    }
  } catch (error) {
    button.disabled = false;
  }
});
