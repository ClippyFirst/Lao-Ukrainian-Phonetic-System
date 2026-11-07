import { test, expect } from "@playwright/test";

test("Lao input produces visible Ukrainian and IPA results", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#output")).toHaveText("к'а");
  await expect(page.locator("#ipa")).toHaveText("kʰaː");
  await expect(page.locator("#analysis-status")).toContainText("ГОТОВО");
});

test("mixed-script input fails closed instead of fabricating output", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ກа");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#analysis-status")).toContainText("НЕ ВСТАНОВЛЕНО");
  await expect(page.locator("#output")).toContainText("не пройшов перевірку");
});

test("clear control restores the empty state", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.locator("#output")).toHaveText("к'а");
  await page.locator("#clear").click();
  await expect(page.locator("#results")).toBeHidden();
  await expect(page.locator("#empty-state")).toBeVisible();
});

test("romanization mode is explicitly separate from IPA-first mode", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#mode-romanization")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#romanization-trace")).toBeVisible();
  await page.locator("#mode-phonetic").click();
  await expect(page.locator("#mode-phonetic")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#output")).toHaveText("к'а");
});


test("keyboard users can reach the main tool through the skip link", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Перейти до інструмента" });
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page.locator("#lao-input")).toBeFocused();
  await page.keyboard.type("ຂາ");
  await expect(page.locator("#output")).toHaveText("к'а");
  for (const selector of ["#example", "#example-complex", "#clear", "#copy", "#mode-phonetic", "#mode-romanization"]) {
    await page.keyboard.press("Tab");
    await expect(page.locator(selector)).toBeFocused();
  }
  await page.keyboard.press("Enter");
  await expect(page.locator("#mode-romanization")).toHaveAttribute("aria-pressed", "true");
});

test("the service exposes named landmarks, controls, and live result announcements", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("banner")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Основна навігація" })).toBeVisible();
  await expect(page.getByRole("main")).toBeVisible();
  await expect(page.getByRole("textbox", { name: "Лаоський текст" })).toBeVisible();
  await expect(page.getByRole("group", { name: "Швидкі приклади" })).toBeVisible();
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.getByRole("group", { name: "Метод українського запису" })).toBeVisible();
  await expect(page.locator("#output")).toHaveAttribute("aria-live", "polite");
  await expect(page.locator("#status")).toHaveAttribute("role", "status");
  await expect(page.locator(".trace-summary")).toHaveCount(2);
});

test("mobile, tablet, and 200-percent-equivalent layouts do not overflow horizontally", async ({ page }) => {
  for (const width of [390, 768, 640]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    await page.locator("#lao-input").fill("ຂາ");
    await expect(page.locator("#output")).toHaveText("к'а");
    const layout = await page.evaluate(() => ({
      viewport: window.innerWidth,
      document: document.documentElement.scrollWidth,
      body: document.body.scrollWidth,
      output: document.querySelector("#output").getBoundingClientRect().right
    }));
    expect(layout.document, `document overflows at ${width}px`).toBeLessThanOrEqual(layout.viewport);
    expect(layout.body, `body overflows at ${width}px`).toBeLessThanOrEqual(layout.viewport);
    expect(layout.output, `output exceeds viewport at ${width}px`).toBeLessThanOrEqual(layout.viewport);
  }
});
